"""Tests for the command-line interface."""

from __future__ import annotations

import io
import json
from typing import TYPE_CHECKING

import pytest

from cyberkb.cli import (
    EXIT_CONFIG,
    EXIT_INCOMPLETE,
    EXIT_NO_CAPACITY,
    EXIT_OK,
    EXIT_POLICY,
    EXIT_USAGE,
    Runtime,
    main,
)
from cyberkb.enrich_state import EnrichState, InFlightMove, load_state, save_state
from cyberkb.frontmatter import Classification
from tests.conftest import write_resource
from tests.llmfakes import KEYS, EchoNetwork, FakeTime, write_catalog

if TYPE_CHECKING:
    from pathlib import Path

    from cyberkb.paths import RepoPaths

NMAP_BODY = (
    "# Nmap guide\n\nNmap network scanner for penetration testing reconnaissance, "
    "host discovery, port scanning and service detection in an authorized pentest engagement.\n"
)
HEURISTIC = Classification("heuristic", 0.4)


def _run(args: list[str], runtime: Runtime | None = None) -> tuple[int, str]:
    """Run the CLI capturing its exit code and output."""
    out = io.StringIO()
    code = main(args, out=out, runtime=runtime or Runtime(env={}))
    return code, out.getvalue()


def _llm(repo: RepoPaths, network: EchoNetwork | None = None) -> Runtime:
    """A runtime with both keys, the echo network and a fake clock; writes the catalog."""
    write_catalog(repo.root)
    time = FakeTime()
    return Runtime(
        env=KEYS,
        transport=network or EchoNetwork(),
        now=time.now,
        clock=time.clock,
        sleep=time.sleep,
    )


def _pending(repo: RepoPaths, *names: str) -> None:
    for index, name in enumerate(names, start=1):
        write_resource(
            repo,
            filename=f"{name}.md",
            id=f"ckb-{index:012x}",
            classification=HEURISTIC,
            summary="",
            body=f"# {name}\n\nNotes {name} about nmap scanning and service detection.\n",
        )


def _report(repo: RepoPaths) -> dict[str, object]:
    (path,) = sorted(repo.ingest_runs.glob("*.json"))
    data: dict[str, object] = json.loads(path.read_text(encoding="utf-8"))
    return data


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    """`--version` prints the version and exits zero."""
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert "cyberkb" in capsys.readouterr().out


def test_no_command_errors() -> None:
    """Invoking with no subcommand is a usage error."""
    with pytest.raises(SystemExit) as exc:
        main([])
    assert exc.value.code == EXIT_USAGE


def test_build_command(repo: RepoPaths) -> None:
    """`build` regenerates artefacts and reports what changed."""
    write_resource(repo)
    code, output = _run(["--repo", str(repo.root), "build"])
    assert code == EXIT_OK
    assert "Rebuilt" in output


def test_build_up_to_date(built_repo: RepoPaths) -> None:
    """`build` on an unchanged repo reports it is up to date."""
    code, output = _run(["--repo", str(built_repo.root), "build"])
    assert code == EXIT_OK
    assert "up to date" in output


def test_build_reports_problems(repo: RepoPaths) -> None:
    """`build` reports library problems and exits non-zero."""
    (repo.library / "stray.md").write_text("x", encoding="utf-8")
    code, output = _run(["--repo", str(repo.root), "build"])
    assert code == EXIT_POLICY
    assert "validation problems" in output


def test_check_clean(built_repo: RepoPaths) -> None:
    """`check` on a clean repo exits zero with no errors."""
    code, output = _run(["--repo", str(built_repo.root), "check"])
    assert code == EXIT_OK
    assert "0 error" in output


def test_check_fails_on_drift(built_repo: RepoPaths) -> None:
    """`check` reports drift and exits non-zero."""
    built_repo.index_json.write_text("{}\n", encoding="utf-8")
    code, output = _run(["--repo", str(built_repo.root), "check"])
    assert code == EXIT_POLICY
    assert "ERROR" in output


def test_check_invalid_taxonomy(repo: RepoPaths) -> None:
    """`check` fails when the taxonomy is invalid."""
    repo.taxonomy.write_text("version: 1\n", encoding="utf-8")
    code, _ = _run(["--repo", str(repo.root), "check"])
    assert code == EXIT_POLICY


def test_ingest_heuristic_flag(repo: RepoPaths) -> None:
    """`--heuristic` files submissions offline, without keys or a report."""
    (repo.inbox / "nmap.md").write_text(NMAP_BODY, encoding="utf-8")
    code, output = _run(["--repo", str(repo.root), "ingest", "--heuristic"])
    assert code == EXIT_OK
    assert "Filed 1" in output
    assert not repo.ingest_runs.exists()


def test_ingest_with_submissions_requires_the_keys(repo: RepoPaths) -> None:
    """Classifying new submissions with an LLM needs both keys: fail fast, clearly."""
    write_catalog(repo.root)
    (repo.inbox / "nmap.md").write_text(NMAP_BODY, encoding="utf-8")
    code, output = _run(["--repo", str(repo.root), "ingest"])
    assert code == EXIT_CONFIG
    assert "missing API key(s): GEMINI_API_KEY, GROQ_API_KEY" in output
    assert (repo.inbox / "nmap.md").exists()


def test_ingest_with_providers_writes_a_report_and_summary(repo: RepoPaths, tmp_path: Path) -> None:
    """With keys, ingest classifies through the engine and reports the run."""
    (repo.inbox / "nmap.md").write_text(NMAP_BODY, encoding="utf-8")
    summary = tmp_path / "summary.md"
    code, output = _run(
        ["--repo", str(repo.root), "ingest", "--run-id", "gh7-1-ingest", "--summary", str(summary)],
        _llm(repo),
    )
    assert code == EXIT_OK
    assert "Filed 1" in output
    report = _report(repo)
    assert report["command"] == "ingest"
    assert report["run_id"] == "gh7-1-ingest"
    assert "`gemma-t-it`" in summary.read_text(encoding="utf-8")
    assert load_state(repo).usage["google:gemma-t-it"].requests == 2


def test_ingest_without_submissions_needs_no_keys(repo: RepoPaths) -> None:
    """A catalog-only rebuild never touches a provider."""
    code, _ = _run(["--repo", str(repo.root), "ingest"])
    assert code == EXIT_OK


def test_ingest_command_rejects(repo: RepoPaths) -> None:
    """`ingest` exits non-zero when a submission is rejected."""
    (repo.inbox / "empty.md").write_text("[[ PAGE 1 ]]\n", encoding="utf-8")
    code, output = _run(["--repo", str(repo.root), "ingest", "--heuristic"])
    assert code == EXIT_POLICY
    assert "rejected" in output


def test_ingest_rejection_is_reported_as_partial(repo: RepoPaths) -> None:
    """With providers, a rejected submission makes the run report partial."""
    (repo.inbox / "empty.md").write_text("[[ PAGE 1 ]]\n", encoding="utf-8")
    (repo.inbox / "nmap.md").write_text(NMAP_BODY, encoding="utf-8")
    code, _ = _run(["--repo", str(repo.root), "ingest"], _llm(repo))
    assert code == EXIT_POLICY
    assert _report(repo)["final_status"] == {
        "status": "partial",
        "reason": "Filed 1, staged 0, rejected 1.",
    }


def test_ingest_build_problem(repo: RepoPaths) -> None:
    """A post-ingest build failure makes `ingest` exit non-zero."""
    (repo.library / "stray.md").write_text("x", encoding="utf-8")
    (repo.inbox / "nmap.md").write_text(NMAP_BODY, encoding="utf-8")
    code, _output = _run(["--repo", str(repo.root), "ingest", "--heuristic"])
    assert code == EXIT_POLICY


def test_classify_command(repo: RepoPaths, tmp_path: Path) -> None:
    """`classify` previews a classification without writing."""
    sample = tmp_path / "sample.md"
    sample.write_text(NMAP_BODY, encoding="utf-8")
    code, output = _run(["--repo", str(repo.root), "classify", "--heuristic", str(sample)])
    assert code == EXIT_OK
    assert "offensive-security" in output
    assert "title:" in output


def test_classify_missing_file(repo: RepoPaths) -> None:
    """`classify` on a missing file is a usage error."""
    code, output = _run(["--repo", str(repo.root), "classify", "--heuristic", "/no/such/file.md"])
    assert code == EXIT_USAGE
    assert "cannot read" in output


def test_classify_uses_the_engine_by_default(repo: RepoPaths, tmp_path: Path) -> None:
    """Without --heuristic, classify previews the LLM answer."""
    sample = tmp_path / "sample.md"
    sample.write_text(NMAP_BODY, encoding="utf-8")
    code, output = _run(["--repo", str(repo.root), "classify", str(sample)], _llm(repo))
    assert code == EXIT_OK
    assert "via llm" in output


def test_enrich_requires_both_keys(repo: RepoPaths) -> None:
    """Enrichment never starts without both keys."""
    write_catalog(repo.root)
    _pending(repo, "a")
    code, output = _run(
        ["--repo", str(repo.root), "enrich"], Runtime(env={"GEMINI_API_KEY": "x" * 20})
    )
    assert code == EXIT_CONFIG
    assert "GROQ_API_KEY" in output
    assert "x" * 20 not in output


def test_enrich_completes_and_records_everything(repo: RepoPaths, tmp_path: Path) -> None:
    """A complete run exits 0 and leaves the ledger, the report and the catalogs."""
    _pending(repo, "a", "b")
    summary = tmp_path / "summary.md"
    code, output = _run(
        [
            "--repo",
            str(repo.root),
            "enrich",
            "--run-id",
            "gh9-1-enrich-c1",
            "--summary",
            str(summary),
        ],
        _llm(repo),
    )
    assert code == EXIT_OK
    assert "Final status: complete" in output
    state = load_state(repo)
    assert state.counts() == {"pending": 0, "enriched": 2, "failed": 0}
    assert state.last_run is not None
    assert state.last_run["status"] == "complete"
    assert state.validations["google:gemma-t-it"].ok
    report = _report(repo)
    assert report["final_status"]["status"] == "complete"  # type: ignore[index]
    assert report["work"]["enriched"] == 2  # type: ignore[index]
    assert {r["status"] for r in report["resources"]} == {"enriched"}  # type: ignore[attr-defined]
    assert "Final status: complete" in summary.read_text(encoding="utf-8")
    assert (repo.root / "index.json").exists()


def test_enrich_limit_is_partial_with_the_incomplete_exit(repo: RepoPaths) -> None:
    """A budget-bounded run exits 5 so the workflow knows to continue."""
    _pending(repo, "a", "b")
    code, output = _run(
        ["--repo", str(repo.root), "enrich", "--limit", "1", "--max-seconds", "3600"], _llm(repo)
    )
    assert code == EXIT_INCOMPLETE
    assert "partial" in output
    assert load_state(repo).counts()["pending"] == 1


def test_enrich_with_every_quota_spent_exits_no_capacity(repo: RepoPaths) -> None:
    """When every model is exhausted the run exits 6 and says why."""
    _pending(repo, "a")
    code, output = _run(
        ["--repo", str(repo.root), "enrich"], _llm(repo, EchoNetwork(google="daily", groq="daily"))
    )
    assert code == EXIT_NO_CAPACITY
    assert "every model is exhausted or failed" in output
    report = _report(repo)
    assert report["failure_breakdown"]["quota_exceeded"] == 3  # type: ignore[index]


def test_enrich_reports_a_recovered_move(repo: RepoPaths) -> None:
    """An interrupted move from a previous run is completed and noted."""
    _pending(repo, "a")
    write_resource(
        repo,
        category="incident-response-and-forensics",
        filename="a.md",
        id="ckb-000000000001",
        classification=HEURISTIC,
        summary="",
    )
    save_state(
        repo,
        EnrichState(
            in_flight=InFlightMove(
                "ckb-000000000001",
                "library/offensive-security/a.md",
                "library/incident-response-and-forensics/a.md",
            )
        ),
        now_iso="2026-10-07T00:00:00Z",
    )
    code, output = _run(["--repo", str(repo.root), "enrich"], _llm(repo))
    assert code == EXIT_OK
    assert "completed interrupted move" in output
    assert _report(repo)["notes"]


def test_enrich_reports_build_problem(repo: RepoPaths) -> None:
    """A post-enrich build failure makes `enrich` exit non-zero."""
    _pending(repo, "a")
    (repo.library / "stray.md").write_text("not a resource", encoding="utf-8")
    code, output = _run(["--repo", str(repo.root), "enrich"], _llm(repo))
    assert code == EXIT_POLICY
    assert "stray.md" in output


def test_enrich_rejects_an_unsafe_run_id(repo: RepoPaths) -> None:
    """The run id becomes a file name and is validated up front."""
    code, output = _run(["--repo", str(repo.root), "enrich", "--run-id", "../x"], _llm(repo))
    assert code == EXIT_CONFIG
    assert "run id" in output


@pytest.mark.parametrize("bad", ["0", "-1"])
def test_enrich_budgets_must_be_positive(repo: RepoPaths, bad: str) -> None:
    """A zero or negative budget is a usage error."""
    with pytest.raises(SystemExit) as exc:
        _run(["--repo", str(repo.root), "enrich", "--limit", bad])
    assert exc.value.code == EXIT_USAGE
    with pytest.raises(SystemExit):
        _run(["--repo", str(repo.root), "enrich", "--max-seconds", bad])


def test_preflight_validates_every_model(repo: RepoPaths, tmp_path: Path) -> None:
    """Preflight probes the whole catalog, prints each verdict and changes no content."""
    _pending(repo, "a")
    summary = tmp_path / "summary.md"
    code, output = _run(
        ["--repo", str(repo.root), "preflight", "--summary", str(summary)], _llm(repo)
    )
    assert code == EXIT_OK
    assert "3 of 3 catalog models are usable" in output
    assert "-> gemma-t-it [active, json_schema]" in output
    assert "| 3 | groq | groq-a | `groq-a` | exact id | active |" in summary.read_text(
        encoding="utf-8"
    )
    assert _report(repo)["command"] == "preflight"
    assert load_state(repo).counts()["pending"] == 0


def test_preflight_without_any_usable_model(repo: RepoPaths) -> None:
    """No usable model is the no-capacity exit."""
    code, output = _run(
        ["--repo", str(repo.root), "preflight"],
        _llm(repo, EchoNetwork(google="error", groq="error")),
    )
    assert code == EXIT_NO_CAPACITY
    assert "0 of 3" in output


def test_config_error_exit(repo: RepoPaths) -> None:
    """A real taxonomy error during a command maps to the config exit code."""
    repo.taxonomy.write_text("version: 1\n", encoding="utf-8")  # structurally invalid
    sample = repo.root / "s.md"
    sample.write_text(NMAP_BODY, encoding="utf-8")
    code, output = _run(["--repo", str(repo.root), "classify", str(sample)])
    assert code == EXIT_CONFIG
    assert "error:" in output


def test_classify_without_tags(repo: RepoPaths, tmp_path: Path) -> None:
    """A document with no detectable tags prints no tags line."""
    sample = tmp_path / "plain.md"
    sample.write_text(
        "# Plain Note\n\n" + " ".join(["lorem ipsum dolor"] * 15) + "\n",
        encoding="utf-8",
    )
    code, output = _run(["--repo", str(repo.root), "classify", "--heuristic", str(sample)])
    assert code == EXIT_OK
    assert "tags:" not in output
