"""Command-line interface: ``cyberkb <command>``.

Commands:

* ``build``    -- regenerate catalogs, README index and category pages.
* ``check``    -- run repository policy checks (CI gate); exits non-zero on error.
* ``ingest``   -- classify and file ``inbox/`` submissions, then build.
* ``classify`` -- preview classification of files without writing (debugging).

Exit codes are stable so CI and scripts can branch on them:
``0`` success, ``1`` policy/validation failure, ``2`` usage error,
``3`` configuration/service error, ``4`` unexpected internal error.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from cyberkb import __version__
from cyberkb.build import build
from cyberkb.checks import Severity, run_checks
from cyberkb.config import IngestConfig
from cyberkb.errors import KBError
from cyberkb.paths import RepoPaths
from cyberkb.sanitize import sanitize_markdown
from cyberkb.taxonomy import load_taxonomy

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import TextIO

    from cyberkb.classify.llm import LLMClassifier
    from cyberkb.taxonomy import Taxonomy

__all__ = ["main"]

EXIT_OK = 0
EXIT_POLICY = 1
EXIT_USAGE = 2
EXIT_CONFIG = 3
EXIT_INTERNAL = 4


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

    classify = sub.add_parser("classify", help="preview classification of files without writing")
    classify.add_argument("paths", nargs="+", type=Path, help="Markdown files to classify")
    classify.add_argument(
        "--heuristic", action="store_true", help="force offline heuristic classification"
    )
    return parser


def _make_classifier(
    taxonomy: Taxonomy, *, force_heuristic: bool, out: TextIO
) -> LLMClassifier | None:
    if force_heuristic:
        return None
    config = IngestConfig.from_env()
    if not config.use_llm:
        print("No GEMINI_API_KEY set; using deterministic heuristic classifier.", file=out)
        return None
    from cyberkb.classify.llm import LLMClassifier  # noqa: PLC0415 -- keep import local to LLM path
    from cyberkb.llm import GeminiClient  # noqa: PLC0415

    client = GeminiClient(
        config.api_key or "",
        config.models,
        max_retries=config.max_retries,
        timeout=config.timeout,
    )
    return LLMClassifier(client, taxonomy)


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


def _cmd_ingest(paths: RepoPaths, args: argparse.Namespace, out: TextIO) -> int:
    from cyberkb.ingest import ingest_inbox  # noqa: PLC0415
    from cyberkb.library import load_library  # noqa: PLC0415

    taxonomy = load_taxonomy(paths.root)
    classifier = _make_classifier(taxonomy, force_heuristic=args.heuristic, out=out)
    config = IngestConfig.from_env()
    taken = frozenset(r.id for r in load_library(paths, taxonomy).resources)
    report = ingest_inbox(
        paths, taxonomy, classifier=classifier, taken_ids=taken, batch_size=config.batch_size
    )
    for outcome in report.outcomes:
        if outcome.destination:
            print(f"  {outcome.status}: {outcome.source} -> {outcome.destination}", file=out)
        else:
            print(f"  {outcome.status}: {outcome.source} ({outcome.reason})", file=out)
    print(f"Filed {report.filed}, staged {report.staged}, rejected {report.rejected}.", file=out)
    build_result = build(paths)
    if not build_result.ok:
        for path, message in build_result.problems:
            print(f"  {path}: {message}", file=out)
        return EXIT_POLICY
    return EXIT_POLICY if report.rejected else EXIT_OK


def _cmd_classify(paths: RepoPaths, args: argparse.Namespace, out: TextIO) -> int:
    from cyberkb.classify.base import Document  # noqa: PLC0415
    from cyberkb.classify.heuristic import classify as heuristic_classify  # noqa: PLC0415

    taxonomy = load_taxonomy(paths.root)
    classifier = _make_classifier(taxonomy, force_heuristic=args.heuristic, out=out)
    documents = []
    for index, file_path in enumerate(args.paths):
        try:
            body = sanitize_markdown(file_path.read_text(encoding="utf-8", errors="replace"))
        except OSError as exc:
            print(f"  cannot read {file_path}: {exc}", file=out)
            return EXIT_USAGE
        documents.append((file_path, Document(str(index), file_path.stem, body)))

    if classifier is None:
        results = [heuristic_classify(doc, taxonomy) for _, doc in documents]
    else:
        results = classifier.classify_batch([doc for _, doc in documents])
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


def main(argv: Sequence[str] | None = None, *, out: TextIO | None = None) -> int:
    """CLI entry point. Returns a process exit code."""
    stream = out if out is not None else sys.stdout
    parser = _build_parser()
    args = parser.parse_args(argv)
    paths = RepoPaths.at(args.repo)
    try:
        if args.command == "build":
            return _cmd_build(paths, stream)
        if args.command == "check":
            return _cmd_check(paths, stream)
        if args.command == "ingest":
            return _cmd_ingest(paths, args, stream)
        return _cmd_classify(paths, args, stream)  # "classify"
    except KBError as exc:
        print(f"error: {exc}", file=stream)
        return EXIT_CONFIG
    except (OSError, ValueError) as exc:  # pragma: no cover - last-resort guard
        print(f"internal error: {exc}", file=stream)
        return EXIT_INTERNAL


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
