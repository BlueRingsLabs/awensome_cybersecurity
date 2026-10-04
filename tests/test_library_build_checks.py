"""Tests for library loading, building and policy checks."""

from __future__ import annotations

from cyberkb.build import build
from cyberkb.checks import Severity, run_checks
from cyberkb.library import load_library
from cyberkb.taxonomy import load_taxonomy
from tests.conftest import FIXED_NOW, write_resource


def _taxonomy(repo):
    return load_taxonomy(repo.root)


# --- load_library ---------------------------------------------------------


def test_load_empty_library(repo) -> None:
    loaded = load_library(repo, _taxonomy(repo))
    assert loaded.resources == ()
    assert loaded.ok


def test_load_missing_library_dir(repo) -> None:
    (repo.library).rmdir()
    loaded = load_library(repo, _taxonomy(repo))
    assert loaded.resources == ()


def test_load_valid_resource(repo) -> None:
    write_resource(repo, filename="a.md")
    loaded = load_library(repo, _taxonomy(repo))
    assert len(loaded.resources) == 1
    assert loaded.ok


def test_load_rejects_stray_file(repo) -> None:
    (repo.library / "stray.md").write_text("x", encoding="utf-8")
    loaded = load_library(repo, _taxonomy(repo))
    assert any("category folder" in msg for _, msg in loaded.problems)


def test_load_rejects_unknown_category_dir(repo) -> None:
    (repo.library / "not-a-category").mkdir()
    loaded = load_library(repo, _taxonomy(repo))
    assert any("not a taxonomy category" in msg for _, msg in loaded.problems)


def test_load_rejects_missing_front_matter(repo) -> None:
    (repo.library / "offensive-security").mkdir(parents=True)
    (repo.library / "offensive-security" / "bad.md").write_text(
        "# No front matter\n", encoding="utf-8"
    )
    loaded = load_library(repo, _taxonomy(repo))
    assert any("front matter" in msg for _, msg in loaded.problems)


def test_load_rejects_category_mismatch(repo) -> None:
    # File physically under malware-analysis but front matter says offensive-security.
    write_resource(repo, category="offensive-security", filename="x.md")
    moved = repo.library / "malware-analysis"
    moved.mkdir(parents=True)
    (moved / "x.md").write_text(
        (repo.library / "offensive-security" / "x.md").read_text(), encoding="utf-8"
    )
    (repo.library / "offensive-security" / "x.md").unlink()
    loaded = load_library(repo, _taxonomy(repo))
    assert any("does not match folder" in msg for _, msg in loaded.problems)


def test_load_detects_duplicate_ids(repo) -> None:
    write_resource(
        repo, filename="a.md", id="ckb-aaaaaaaaaaaa", body="# A\n\nunique alpha content here"
    )
    write_resource(
        repo, filename="b.md", id="ckb-aaaaaaaaaaaa", body="# B\n\nunique beta content here"
    )
    loaded = load_library(repo, _taxonomy(repo))
    assert any("duplicate id" in msg for _, msg in loaded.problems)


def test_load_detects_duplicate_bodies(repo) -> None:
    write_resource(
        repo, filename="a.md", id="ckb-aaaaaaaaaaaa", body="# Same\n\nidentical body text"
    )
    write_resource(
        repo, filename="b.md", id="ckb-bbbbbbbbbbbb", body="# Same\n\nidentical body text"
    )
    loaded = load_library(repo, _taxonomy(repo))
    assert any("identical body" in msg for _, msg in loaded.problems)


def test_load_skips_category_readme(repo) -> None:
    write_resource(repo, filename="a.md")
    (repo.library / "offensive-security" / "README.md").write_text(
        "# generated\n", encoding="utf-8"
    )
    loaded = load_library(repo, _taxonomy(repo))
    assert len(loaded.resources) == 1


# --- build ----------------------------------------------------------------


def test_build_generates_all_artefacts(repo) -> None:
    write_resource(repo)
    result = build(repo, generated_at=FIXED_NOW)
    assert result.ok
    assert repo.index_json.exists()
    assert repo.index_yaml.exists()
    assert (repo.library / "offensive-security" / "README.md").exists()
    assert "offensive-security" in {name.split("/")[1] for name in result.changed if "/" in name}


def test_build_is_idempotent(repo) -> None:
    write_resource(repo)
    build(repo, generated_at=FIXED_NOW)
    second = build(repo)  # fresh timestamp, but content unchanged
    assert second.changed == ()


def test_build_aborts_on_problems(repo) -> None:
    (repo.library / "stray.md").write_text("x", encoding="utf-8")
    result = build(repo)
    assert not result.ok
    assert result.problems


def test_build_without_readme(repo) -> None:
    repo.readme.unlink()
    write_resource(repo)
    result = build(repo, generated_at=FIXED_NOW)
    assert result.ok
    assert repo.readme.exists()


# --- checks ---------------------------------------------------------------


def test_checks_clean_repo(built_repo) -> None:
    report = run_checks(built_repo, generated_at=FIXED_NOW)
    assert report.ok
    assert report.resource_count == 1


def test_checks_detects_drift(built_repo) -> None:
    built_repo.index_json.write_text('{"stale": true}\n', encoding="utf-8")
    report = run_checks(built_repo, generated_at=FIXED_NOW)
    assert not report.ok
    assert any("out of date" in f.message for f in report.errors)


def test_checks_missing_generated_file(built_repo) -> None:
    built_repo.index_yaml.unlink()
    report = run_checks(built_repo, generated_at=FIXED_NOW)
    assert any("missing" in f.message for f in report.errors)


def test_checks_invalid_taxonomy(repo) -> None:
    repo.taxonomy.write_text("version: 1\n", encoding="utf-8")
    report = run_checks(repo)
    assert not report.ok
    assert report.resource_count == 0


def test_checks_restricted_license_is_error(repo) -> None:
    write_resource(repo, license="LicenseRef-All-Rights-Reserved")
    build(repo, generated_at=FIXED_NOW)
    report = run_checks(repo, generated_at=FIXED_NOW)
    assert any("forbids redistribution" in f.message for f in report.errors)


def test_checks_noassertion_is_warning(repo) -> None:
    write_resource(repo, license="NOASSERTION")
    build(repo, generated_at=FIXED_NOW)
    report = run_checks(repo, generated_at=FIXED_NOW)
    assert any(f.severity is Severity.WARNING for f in report.warnings)
    assert report.ok  # warnings do not fail the gate


def test_checks_active_content_is_warning(repo) -> None:
    write_resource(
        repo, body="# Doc\n\nHere is <script>alert(1)</script> inline.\n", filename="x.md"
    )
    build(repo, generated_at=FIXED_NOW)
    report = run_checks(repo, generated_at=FIXED_NOW)
    assert any("active/executable" in f.message for f in report.warnings)
    assert report.ok  # advisory only, does not fail the gate


def test_checks_readme_drift(built_repo) -> None:
    built_repo.readme.write_text("# Broken\n\nno markers\n", encoding="utf-8")
    report = run_checks(built_repo, generated_at=FIXED_NOW)
    assert any("AUTO-INDEX" in f.message or "README" in f.path for f in report.errors)


def test_checks_category_page_drift(built_repo) -> None:
    (built_repo.library / "offensive-security" / "README.md").write_text(
        "stale\n", encoding="utf-8"
    )
    report = run_checks(built_repo, generated_at=FIXED_NOW)
    assert any("category page" in f.message for f in report.errors)


def test_checks_missing_category_page(built_repo) -> None:
    (built_repo.library / "offensive-security" / "README.md").unlink()
    report = run_checks(built_repo, generated_at=FIXED_NOW)
    assert any("category page is missing" in f.message for f in report.errors)


def test_checks_missing_readme(built_repo) -> None:
    built_repo.readme.unlink()
    report = run_checks(built_repo, generated_at=FIXED_NOW)
    assert any(f.path == "README.md" for f in report.errors)
