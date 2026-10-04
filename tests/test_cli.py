"""Tests for the command-line interface."""

from __future__ import annotations

import io

import pytest

from cyberkb.cli import (
    EXIT_CONFIG,
    EXIT_OK,
    EXIT_POLICY,
    EXIT_USAGE,
    main,
)
from tests.conftest import write_resource

NMAP_BODY = (
    "# Nmap guide\n\nNmap network scanner for penetration testing reconnaissance, "
    "host discovery, port scanning and service detection in an authorized pentest engagement.\n"
)


def _run(args: list[str]) -> tuple[int, str]:
    out = io.StringIO()
    code = main(args, out=out)
    return code, out.getvalue()


def test_version(capsys) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert "cyberkb" in capsys.readouterr().out


def test_no_command_errors() -> None:
    with pytest.raises(SystemExit) as exc:
        main([])
    assert exc.value.code == EXIT_USAGE


def test_build_command(repo) -> None:
    write_resource(repo)
    code, output = _run(["--repo", str(repo.root), "build"])
    assert code == EXIT_OK
    assert "Rebuilt" in output


def test_build_up_to_date(built_repo) -> None:
    code, output = _run(["--repo", str(built_repo.root), "build"])
    assert code == EXIT_OK
    assert "up to date" in output


def test_build_reports_problems(repo) -> None:
    (repo.library / "stray.md").write_text("x", encoding="utf-8")
    code, output = _run(["--repo", str(repo.root), "build"])
    assert code == EXIT_POLICY
    assert "validation problems" in output


def test_check_clean(built_repo) -> None:
    code, output = _run(["--repo", str(built_repo.root), "check"])
    assert code == EXIT_OK
    assert "0 error" in output


def test_check_fails_on_drift(built_repo) -> None:
    built_repo.index_json.write_text("{}\n", encoding="utf-8")
    code, output = _run(["--repo", str(built_repo.root), "check"])
    assert code == EXIT_POLICY
    assert "ERROR" in output


def test_check_invalid_taxonomy(repo) -> None:
    repo.taxonomy.write_text("version: 1\n", encoding="utf-8")
    code, _ = _run(["--repo", str(repo.root), "check"])
    assert code == EXIT_POLICY


def test_ingest_command(repo) -> None:
    (repo.inbox / "nmap.md").write_text(NMAP_BODY, encoding="utf-8")
    code, output = _run(["--repo", str(repo.root), "ingest"])
    assert code == EXIT_OK
    assert "Filed 1" in output
    assert "heuristic" in output


def test_ingest_command_rejects(repo) -> None:
    (repo.inbox / "empty.md").write_text("[[ PAGE 1 ]]\n", encoding="utf-8")
    code, output = _run(["--repo", str(repo.root), "ingest"])
    assert code == EXIT_POLICY
    assert "rejected" in output


def test_ingest_heuristic_flag(repo, monkeypatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "should-be-ignored")
    (repo.inbox / "nmap.md").write_text(NMAP_BODY, encoding="utf-8")
    code, _output = _run(["--repo", str(repo.root), "ingest", "--heuristic"])
    assert code == EXIT_OK


def test_ingest_build_problem(repo, monkeypatch) -> None:
    # Force a post-ingest build failure by leaving a stray file in library/.
    (repo.library / "stray.md").write_text("x", encoding="utf-8")
    (repo.inbox / "nmap.md").write_text(NMAP_BODY, encoding="utf-8")
    code, _output = _run(["--repo", str(repo.root), "ingest"])
    assert code == EXIT_POLICY


def test_classify_command(repo, tmp_path) -> None:
    sample = tmp_path / "sample.md"
    sample.write_text(NMAP_BODY, encoding="utf-8")
    code, output = _run(["--repo", str(repo.root), "classify", str(sample)])
    assert code == EXIT_OK
    assert "offensive-security" in output
    assert "title:" in output


def test_classify_missing_file(repo) -> None:
    code, output = _run(["--repo", str(repo.root), "classify", "/no/such/file.md"])
    assert code == EXIT_USAGE
    assert "cannot read" in output


def test_classify_uses_llm_when_key_present(repo, tmp_path, monkeypatch) -> None:
    import json as _json

    from cyberkb import llm

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
        "candidates": [{"content": {"parts": [{"text": _json.dumps({"classifications": [item]})}]}}]
    }

    def fake_post(self, url, body, headers, timeout):
        return llm.HttpResponse(200, _json.dumps(payload).encode())

    monkeypatch.setattr(llm.UrllibTransport, "post", fake_post)
    code, output = _run(["--repo", str(repo.root), "classify", str(sample)])
    assert code == EXIT_OK
    assert "LLM Guide" in output


def test_config_error_exit(repo, monkeypatch) -> None:
    from cyberkb import cli

    def boom(_root):
        from cyberkb.errors import TaxonomyError

        raise TaxonomyError("broken")

    monkeypatch.setattr(cli, "load_taxonomy", boom)
    sample = repo.root / "s.md"
    sample.write_text(NMAP_BODY, encoding="utf-8")
    code, output = _run(["--repo", str(repo.root), "classify", str(sample)])
    assert code == EXIT_CONFIG
    assert "error:" in output


def test_classify_without_tags(repo, tmp_path) -> None:
    # A document with no detectable tags exercises the empty-tags branch.
    sample = tmp_path / "plain.md"
    sample.write_text(
        "# Plain Note\n\n" + " ".join(["lorem ipsum dolor"] * 15) + "\n", encoding="utf-8"
    )
    code, output = _run(["--repo", str(repo.root), "classify", str(sample)])
    assert code == EXIT_OK
    assert "tags:" not in output
