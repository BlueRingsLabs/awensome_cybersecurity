"""Command-line interface: ``cyberkb <command>``.

Commands:

* ``build``     -- regenerate catalogs, README index and category pages.
* ``check``     -- run repository policy checks (CI gate); exits non-zero on error.
* ``ingest``    -- classify and file ``inbox/`` submissions, then build.
* ``enrich``    -- classify pending library resources with an LLM and backfill summaries.
* ``preflight`` -- discover and validate every catalog model now; changes no content.
* ``classify``  -- preview classification of files without writing (debugging).

Exit codes are stable so CI and scripts can branch on them:

* ``0`` success (``enrich``: every eligible resource is enriched);
* ``1`` policy/validation failure; ``2`` usage error;
* ``3`` configuration or service error (missing/rejected key, bad catalog);
* ``4`` unexpected internal error;
* ``5`` ``enrich`` incomplete because its run budget ended — more can be done now;
* ``6`` incomplete with no capacity left this run (every model exhausted or
  failed, or the remaining resources failed on every usable model);
  ``preflight`` with no usable model.
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cyberkb import __version__
from cyberkb.build import build
from cyberkb.checks import Severity, run_checks
from cyberkb.config import IngestConfig
from cyberkb.enrich_state import load_state, recover, save_state
from cyberkb.errors import KBError
from cyberkb.obslog import StructuredLogger, utc_now_iso
from cyberkb.paths import RepoPaths
from cyberkb.pipeline import build_classifier
from cyberkb.runreport import build_run_report, default_run_id, safe_run_id, write_run_report
from cyberkb.sanitize import sanitize_markdown
from cyberkb.taxonomy import load_taxonomy

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping, Sequence
    from typing import TextIO

    from cyberkb.classify.llm import LLMClassifier
    from cyberkb.enrich import EnrichReport
    from cyberkb.enrich_state import EnrichState
    from cyberkb.providers.catalog import ModelCatalog
    from cyberkb.providers.http import Transport
    from cyberkb.providers.rotation import RotationEngine
    from cyberkb.taxonomy import Taxonomy

__all__ = ["Runtime", "main"]

EXIT_OK = 0
EXIT_POLICY = 1
EXIT_USAGE = 2
EXIT_CONFIG = 3
EXIT_INTERNAL = 4
EXIT_INCOMPLETE = 5
EXIT_NO_CAPACITY = 6


@dataclass(frozen=True, slots=True)
class Runtime:
    """Process-level collaborators, injectable so tests never touch the network or sleep."""

    env: Mapping[str, str] | None = None
    transport: Transport | None = None
    now: Callable[[], datetime] = field(default=lambda: datetime.now(UTC))
    clock: Callable[[], float] = time.monotonic
    sleep: Callable[[float], None] = time.sleep


def _positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        msg = "must be a positive integer"
        raise argparse.ArgumentTypeError(msg)
    return number


def _positive_float(value: str) -> float:
    number = float(value)
    if number <= 0:
        msg = "must be a positive number of seconds"
        raise argparse.ArgumentTypeError(msg)
    return number


def _add_run_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--run-id", default=None, help="id used in the run report file name (default: automatic)"
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=None,
        help="append a Markdown summary to this file (e.g. $GITHUB_STEP_SUMMARY)",
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cyberkb", description="awesome_cybersecurity knowledge base engine."
    )
    parser.add_argument("--version", action="version", version=f"cyberkb {__version__}")
    parser.add_argument(
        "--repo", type=Path, default=Path.cwd(), help="repository root (default: current directory)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("build", help="regenerate catalogs, README index and category pages")
    sub.add_parser("check", help="run repository policy checks (non-zero exit on failure)")

    ingest = sub.add_parser("ingest", help="classify and file inbox/ submissions, then build")
    ingest.add_argument(
        "--heuristic", action="store_true", help="force offline heuristic classification"
    )
    _add_run_options(ingest)

    enrich = sub.add_parser("enrich", help="LLM-classify pending resources and backfill summaries")
    enrich.add_argument(
        "--force", action="store_true", help="also re-enrich resources already classified by an LLM"
    )
    enrich.add_argument(
        "--limit", type=_positive_int, default=None, help="attempt at most N resources this run"
    )
    enrich.add_argument(
        "--max-seconds",
        type=_positive_float,
        default=None,
        dest="max_seconds",
        help="start no new request after this many seconds, so the run ends and commits",
    )
    _add_run_options(enrich)

    preflight = sub.add_parser(
        "preflight", help="discover and validate every catalog model now (changes no content)"
    )
    _add_run_options(preflight)

    classify = sub.add_parser("classify", help="preview classification of files without writing")
    classify.add_argument("paths", nargs="+", type=Path, help="Markdown files to classify")
    classify.add_argument(
        "--heuristic", action="store_true", help="force offline heuristic classification"
    )
    return parser


@dataclass(slots=True)
class _Session:
    """One LLM-using command: its run id, ledger, classifier and timing."""

    paths: RepoPaths
    runtime: Runtime
    out: TextIO
    run_id: str
    started_at: str
    state: EnrichState
    classifier: LLMClassifier
    catalog: ModelCatalog
    notes: list[str]

    @property
    def engine(self) -> RotationEngine:
        return self.classifier.engine

    def persist(self, *, status: str | None = None, reason: str = "") -> None:
        """Save per-model usage/validations (and the run outcome) to the ledger."""
        engine = self.engine
        self.state.usage = engine.usage()
        self.state.validations = engine.validations()
        finished = utc_now_iso(self.runtime.now())
        if status is not None:
            self.state.last_run = {
                "run_id": self.run_id,
                "started_at": self.started_at,
                "finished_at": finished,
                "status": status,
                "reason": reason,
                "retries": engine.retry_summary(),
            }
        save_state(self.paths, self.state, now_iso=finished)

    def report(self, command: str, *, status: str, reason: str, **sections: Any) -> Path:  # noqa: ANN401
        """Write the run report and say where."""
        report = build_run_report(
            command=command,
            run_id=self.run_id,
            started_at=self.started_at,
            finished_at=utc_now_iso(self.runtime.now()),
            status=status,
            reason=reason,
            catalog=self.catalog,
            engine=self.engine,
            notes=self.notes,
            **sections,
        )
        destination = write_run_report(self.paths, report)
        print(
            f"Run report written to {destination.relative_to(self.paths.root).as_posix()}",
            file=self.out,
        )
        return destination


def _session(
    paths: RepoPaths, taxonomy: Taxonomy, args: argparse.Namespace, out: TextIO, runtime: Runtime
) -> _Session:
    """Load the ledger, build the classifier and discover the live models (fails fast)."""
    now = runtime.now()
    run_id = safe_run_id(args.run_id) if args.run_id else default_run_id(now, runtime.env)
    state = load_state(paths)
    notes: list[str] = []
    recovered = recover(paths, state)
    if recovered:
        notes.append(recovered)
        print(f"  {recovered}", file=out)
    config = IngestConfig.from_env(runtime.env)
    classifier, catalog = build_classifier(
        paths,
        taxonomy,
        config,
        logger=StructuredLogger(out, now=runtime.now),
        env=runtime.env,
        usage=state.usage,
        validations=state.validations,
        transport=runtime.transport,
        clock=runtime.clock,
        sleep=runtime.sleep,
        now=runtime.now,
    )
    return _Session(
        paths, runtime, out, run_id, utc_now_iso(now), state, classifier, catalog, notes
    )


def _model_rows(engine: RotationEngine) -> list[str]:
    rows = []
    for model in engine.model_report():
        api = model["api_id"] or "—"
        detail = model["reason"] or (f"mode {model['mode']}" if model["mode"] else "")
        rows.append(
            f"| {model['priority']} | {model['provider']} | {model['declared_name']} | `{api}` "
            f"| {model['rule']} | {model['status']} | {detail} |"
        )
    return rows


def _write_summary(
    target: Path | None, title: str, lines: Sequence[str], engine: RotationEngine
) -> None:
    if target is None:
        return
    body = [
        f"## {title}",
        "",
        *lines,
        "",
        "| # | Provider | Declared model | API id | Resolved by | Status | Detail |",
        "| ---: | --- | --- | --- | --- | --- | --- |",
        *_model_rows(engine),
        "",
    ]
    with target.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(body) + "\n")


def _cmd_build(paths: RepoPaths, out: TextIO) -> int:
    result = build(paths)
    if not result.ok:
        print("Build aborted: the library has validation problems:", file=out)
        for path, message in result.problems:
            print(f"  {path}: {message}", file=out)
        return EXIT_POLICY
    if result.changed:
        print(
            f"Rebuilt {len(result.changed)} file(s) from {result.resource_count} resources:",
            file=out,
        )
        for name in result.changed:
            print(f"  updated {name}", file=out)
    else:
        print(f"Already up to date ({result.resource_count} resources).", file=out)
    return EXIT_OK


def _cmd_check(paths: RepoPaths, out: TextIO) -> int:
    report = run_checks(paths)
    for finding in report.findings:
        marker = "ERROR" if finding.severity is Severity.ERROR else "warn"
        print(f"  [{marker}] {finding.path}: {finding.message}", file=out)
    print(
        f"Checked {report.resource_count} resources: "
        f"{len(report.errors)} error(s), {len(report.warnings)} warning(s).",
        file=out,
    )
    return EXIT_OK if report.ok else EXIT_POLICY


def _rebuild(paths: RepoPaths, out: TextIO) -> bool:
    result = build(paths)
    for path, message in result.problems:
        print(f"  {path}: {message}", file=out)
    return result.ok


def _cmd_ingest(paths: RepoPaths, args: argparse.Namespace, out: TextIO, runtime: Runtime) -> int:
    from cyberkb.ingest import discover_submissions, ingest_inbox  # noqa: PLC0415
    from cyberkb.library import load_library  # noqa: PLC0415

    taxonomy = load_taxonomy(paths.root)
    config = IngestConfig.from_env(runtime.env)
    # The classifier (key check + model discovery) is built only when there is
    # something to classify, so a catalog-only rebuild never spends quota.
    session = None
    if discover_submissions(paths) and not args.heuristic:
        session = _session(paths, taxonomy, args, out, runtime)
    taken = frozenset(r.id for r in load_library(paths, taxonomy).resources)
    report = ingest_inbox(
        paths,
        taxonomy,
        classifier=session.classifier if session else None,
        taken_ids=taken,
        batch_size=config.batch_size,
    )
    for outcome in report.outcomes:
        if outcome.destination:
            print(f"  {outcome.status}: {outcome.source} -> {outcome.destination}", file=out)
        else:
            print(f"  {outcome.status}: {outcome.source} ({outcome.reason})", file=out)
    summary = f"Filed {report.filed}, staged {report.staged}, rejected {report.rejected}."
    print(summary, file=out)
    if session is not None:
        status = "complete" if not report.rejected else "partial"
        session.persist()
        session.report("ingest", status=status, reason=summary)
        _write_summary(args.summary, "Ingest", [summary], session.engine)
    if not _rebuild(paths, out):
        return EXIT_POLICY
    return EXIT_POLICY if report.rejected else EXIT_OK


def _enrich_exit(report: EnrichReport) -> int:
    if report.final_status == "complete":
        return EXIT_OK
    if report.budget_reached and not report.capacity_exhausted:
        return EXIT_INCOMPLETE
    return EXIT_NO_CAPACITY


def _cmd_enrich(paths: RepoPaths, args: argparse.Namespace, out: TextIO, runtime: Runtime) -> int:
    from cyberkb.enrich import EnrichStatus, enrich_library  # noqa: PLC0415

    taxonomy = load_taxonomy(paths.root)
    session = _session(paths, taxonomy, args, out, runtime)
    report = enrich_library(
        paths,
        taxonomy,
        session.classifier,
        session.state,
        force=args.force,
        limit=args.limit,
        max_seconds=args.max_seconds,
        clock=runtime.clock,
        now=runtime.now,
    )
    for outcome in report.outcomes:
        if outcome.status in (EnrichStatus.ENRICHED, EnrichStatus.FAILED):
            print(f"  {outcome.status}: {outcome.path} ({outcome.detail})", file=out)
    counts = session.state.counts()
    work = {
        "eligible": sum(counts.values()),
        "manual_skipped": report.skipped,
        "enriched": counts["enriched"],
        "pending": counts["pending"],
        "failed": counts["failed"],
        "this_run": {
            "enriched": report.enriched,
            "failed": report.failed,
            "deferred": report.deferred,
        },
    }
    lines = [
        f"Enriched {report.enriched}, failed {report.failed}, deferred {report.deferred} this run.",
        (
            f"Ledger: {counts['enriched']} enriched, {counts['pending']} pending, "
            f"{counts['failed']} failed ({report.skipped} manual, out of scope)."
        ),
        f"Final status: {report.final_status} — {report.reason}.",
    ]
    for line in lines:
        print(line, file=out)
    session.persist(status=report.final_status, reason=report.reason)
    resources = [
        o.to_dict()
        for o in report.outcomes
        if o.status not in (EnrichStatus.UNCHANGED, EnrichStatus.SKIPPED)
    ]
    session.report(
        "enrich", status=report.final_status, reason=report.reason, work=work, resources=resources
    )
    _write_summary(args.summary, "Enrich", lines, session.engine)
    if not _rebuild(paths, out):
        return EXIT_POLICY
    return _enrich_exit(report)


def _cmd_preflight(
    paths: RepoPaths, args: argparse.Namespace, out: TextIO, runtime: Runtime
) -> int:
    taxonomy = load_taxonomy(paths.root)
    session = _session(paths, taxonomy, args, out, runtime)
    session.engine.validate_all()
    models = session.engine.model_report()
    active = [m for m in models if m["status"] == "active"]
    for model in models:
        print(
            f"  [{model['priority']:>2}] {model['provider']:<6} {model['declared_name']:<24} "
            f"-> {model['api_id'] or '(not listed)'} [{model['status']}"
            f"{', ' + model['mode'] if model['mode'] else ''}] {model['reason']}",
            file=out,
        )
    reason = f"{len(active)} of {len(models)} catalog models are usable"
    print(f"Preflight: {reason}.", file=out)
    status = "complete" if active else "failed"
    session.persist()
    session.report("preflight", status=status, reason=reason)
    _write_summary(args.summary, "Preflight", [f"{reason}."], session.engine)
    return EXIT_OK if active else EXIT_NO_CAPACITY


def _cmd_classify(paths: RepoPaths, args: argparse.Namespace, out: TextIO, runtime: Runtime) -> int:
    from cyberkb.classify.base import Document  # noqa: PLC0415
    from cyberkb.classify.heuristic import classify as heuristic_classify  # noqa: PLC0415

    taxonomy = load_taxonomy(paths.root)
    documents = []
    for index, file_path in enumerate(args.paths):
        try:
            body = sanitize_markdown(file_path.read_text(encoding="utf-8", errors="replace"))
        except OSError as exc:
            print(f"  cannot read {file_path}: {exc}", file=out)
            return EXIT_USAGE
        documents.append((file_path, Document(str(index), file_path.stem, body)))
    if args.heuristic:
        results = [heuristic_classify(doc, taxonomy) for _, doc in documents]
    else:
        args.run_id = None
        session = _session(paths, taxonomy, args, out, runtime)
        results = session.classifier.classify_batch([doc for _, doc in documents])
    for (file_path, _), result in zip(documents, results, strict=True):
        print(
            f"  {file_path.name}: {result.category} / {result.format} / {result.language} "
            f"(confidence {result.confidence:.2f}, via {result.method})",
            file=out,
        )
        print(f"    title: {result.title}", file=out)
        if result.tags:
            print(f"    tags: {', '.join(result.tags)}", file=out)
    return EXIT_OK


def main(
    argv: Sequence[str] | None = None,
    *,
    out: TextIO | None = None,
    runtime: Runtime | None = None,
) -> int:
    """CLI entry point. Returns a process exit code."""
    stream = out if out is not None else sys.stdout
    rt = runtime or Runtime()
    parser = _build_parser()
    args = parser.parse_args(argv)
    paths = RepoPaths.at(args.repo)
    dispatch = {
        "build": lambda: _cmd_build(paths, stream),
        "check": lambda: _cmd_check(paths, stream),
        "ingest": lambda: _cmd_ingest(paths, args, stream, rt),
        "enrich": lambda: _cmd_enrich(paths, args, stream, rt),
        "preflight": lambda: _cmd_preflight(paths, args, stream, rt),
        "classify": lambda: _cmd_classify(paths, args, stream, rt),
    }
    try:
        return dispatch[args.command]()
    except KBError as exc:
        print(f"error: {exc}", file=stream)
        return EXIT_CONFIG
    except (OSError, ValueError) as exc:  # pragma: no cover - last-resort guard
        print(f"internal error: {exc}", file=stream)
        return EXIT_INTERNAL


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
