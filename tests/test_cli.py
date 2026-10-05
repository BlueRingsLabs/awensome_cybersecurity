"""Tests for the command-line interface."""

from __future__ import annotations

import io
import json
from typing import TYPE_CHECKING

import pytest

from cyberkb import cli, llm
from cyberkb.cli import EXIT_CONFIG, EXIT_OK, EXIT_POLICY, EXIT_USAGE, main
from cyberkb.errors import TaxonomyError
from tests.conftest import write_resource

if TYPE_CHECKING:
    from pathlib import Path

    from cyberkb.paths import RepoPaths

NMAP_BODY = (
    "# Nmap guide\n\nNmap network scanner for penetration testing reconnaissance, "
    "host discovery, port scanning and service detection in an authorized pentest engagement.\n"
)


def _run(args: list[str]) -> tuple[int, str]:
    """Run the CLI capturing its exit code and output."""
    out = io.StringIO()
    code = main(args, out=out)
    return code, out.getvalue()


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


def test_ingest_command(repo: RepoPaths) -> None:
    """`ingest` files a submission using the heuristic when no key is set."""
    (repo.inbox / "nmap.md").write_text(NMAP_BODY, encoding="utf-8")
    code, output = _run(["--repo", str(repo.root), "ingest"])
    assert code == EXIT_OK
    assert "Filed 1" in output
    assert "heuristic" in output


def test_ingest_command_rejects(repo: RepoPaths) -> None:
    """`ingest` exits non-zero when a submission is rejected."""
    (repo.inbox / "empty.md").write_text("[[ PAGE 1 ]]\n", encoding="utf-8")
    code, output = _run(["--repo", str(repo.root), "ingest"])
    assert code == EXIT_POLICY
    assert "rejected" in output


def test_ingest_heuristic_flag(repo: RepoPaths, monkeypatch: pytest.MonkeyPatch) -> None:
    """`--heuristic` forces offline classification even when a key is set."""
    monkeypatch.setenv("GEMINI_API_KEY", "should-be-ignored")
    (repo.inbox / "nmap.md").write_text(NMAP_BODY, encoding="utf-8")
    code, _output = _run(["--repo", str(repo.root), "ingest", "--heuristic"])
    assert code == EXIT_OK


def test_ingest_build_problem(repo: RepoPaths) -> None:
    """A post-ingest build failure makes `ingest` exit non-zero."""
    (repo.library / "stray.md").write_text("x", encoding="utf-8")
    (repo.inbox / "nmap.md").write_text(NMAP_BODY, encoding="utf-8")
    code, _output = _run(["--repo", str(repo.root), "ingest"])
    assert code == EXIT_POLICY


def test_classify_command(repo: RepoPaths, tmp_path: Path) -> None:
    """`classify` previews a classification without writing."""
    sample = tmp_path / "sample.md"
    sample.write_text(NMAP_BODY, encoding="utf-8")
    code, output = _run(["--repo", str(repo.root), "classify", str(sample)])
    assert code == EXIT_OK
    assert "offensive-security" in output
    assert "title:" in output


def test_classify_missing_file(repo: RepoPaths) -> None:
    """`classify` on a missing file is a usage error."""
    code, output = _run(["--repo", str(repo.root), "classify", "/no/such/file.md"])
    assert code == EXIT_USAGE
    assert "cannot read" in output


def test_classify_uses_llm_when_key_present(
    repo: RepoPaths,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """With a key set, `classify` uses the LLM transport (here faked)."""
    sample = tmp_path / "s.md"
    sample.write_text(NMAP_BODY, encoding="utf-8")
    monkeypatch.setenv("GEMINI_API_KEY", "key")

    item = {
        "ref": "0",
        "title": "LLM Guide",
        "category": "offensive-security",
        "format": "guide",
        "language": "en",
        "tags": ["nmap"],
        "summary": "s",
        "confidence": 0.9,
    }
    payload = {
        "candidates": [{"content": {"parts": [{"text": json.dumps({"classifications": [item]})}]}}],
    }

    def fake_post(
        _self: llm.UrllibTransport,
        _url: str,
        _body: bytes,
        _headers: object,
        _timeout: float,
    ) -> llm.HttpResponse:
        return llm.HttpResponse(200, json.dumps(payload).encode())

    monkeypatch.setattr(llm.UrllibTransport, "post", fake_post)
    code, output = _run(["--repo", str(repo.root), "classify", str(sample)])
    assert code == EXIT_OK
    assert "LLM Guide" in output


def test_config_error_exit(repo: RepoPaths, monkeypatch: pytest.MonkeyPatch) -> None:
    """A KBError raised during a command maps to the config exit code."""

    def boom(_root: Path) -> None:
        msg = "broken"
        raise TaxonomyError(msg)

    monkeypatch.setattr(cli, "load_taxonomy", boom)
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
    code, output = _run(["--repo", str(repo.root), "classify", str(sample)])
    assert code == EXIT_OK
    assert "tags:" not in output
