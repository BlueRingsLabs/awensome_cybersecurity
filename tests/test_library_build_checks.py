"""Tests for library loading, building and policy checks."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cyberkb.build import build
from cyberkb.checks import REFERENCE_STUB_MAX_WORDS, Severity, run_checks
from cyberkb.library import load_library
from cyberkb.taxonomy import load_taxonomy
from tests.conftest import FIXED_NOW, write_resource

if TYPE_CHECKING:
    from cyberkb.paths import RepoPaths
    from cyberkb.taxonomy import Taxonomy


def _taxonomy(repo: RepoPaths) -> Taxonomy:
    """Load the taxonomy for a test repository."""
    return load_taxonomy(repo.root)


# --- load_library ---------------------------------------------------------


def test_load_empty_library(repo: RepoPaths) -> None:
    """An empty library loads cleanly with no resources."""
    loaded = load_library(repo, _taxonomy(repo))
    assert loaded.resources == ()
    assert loaded.ok


def test_load_missing_library_dir(repo: RepoPaths) -> None:
    """A missing library directory yields no resources and no error."""
    repo.library.rmdir()
    loaded = load_library(repo, _taxonomy(repo))
    assert loaded.resources == ()


def test_load_valid_resource(repo: RepoPaths) -> None:
    """A valid document loads as one resource."""
    write_resource(repo, filename="a.md")
    loaded = load_library(repo, _taxonomy(repo))
    assert len(loaded.resources) == 1
    assert loaded.ok


def test_load_rejects_stray_file(repo: RepoPaths) -> None:
    """A Markdown file directly under library/ is flagged."""
    (repo.library / "stray.md").write_text("x", encoding="utf-8")
    loaded = load_library(repo, _taxonomy(repo))
    assert any("category folder" in msg for _, msg in loaded.problems)


def test_load_rejects_unknown_category_dir(repo: RepoPaths) -> None:
    """A directory that is not a taxonomy category is flagged."""
    (repo.library / "not-a-category").mkdir()
    loaded = load_library(repo, _taxonomy(repo))
    assert any("not a taxonomy category" in msg for _, msg in loaded.problems)


def test_load_rejects_missing_front_matter(repo: RepoPaths) -> None:
    """A document with no front matter is flagged."""
    (repo.library / "offensive-security").mkdir(parents=True)
    (repo.library / "offensive-security" / "bad.md").write_text(
        "# No front matter\n",
        encoding="utf-8",
    )
    loaded = load_library(repo, _taxonomy(repo))
    assert any("front matter" in msg for _, msg in loaded.problems)


def test_load_rejects_category_mismatch(repo: RepoPaths) -> None:
    """A document whose front-matter category differs from its folder is flagged."""
    write_resource(repo, category="offensive-security", filename="x.md")
    moved = repo.library / "malware-analysis"
    moved.mkdir(parents=True)
    (moved / "x.md").write_text(
        (repo.library / "offensive-security" / "x.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (repo.library / "offensive-security" / "x.md").unlink()
    loaded = load_library(repo, _taxonomy(repo))
    assert any("does not match folder" in msg for _, msg in loaded.problems)


def test_load_detects_duplicate_ids(repo: RepoPaths) -> None:
    """Two resources sharing an id are flagged as duplicates."""
    write_resource(repo, filename="a.md", id="ckb-aaaaaaaaaaaa", body="# A\n\nunique alpha content")
    write_resource(repo, filename="b.md", id="ckb-aaaaaaaaaaaa", body="# B\n\nunique beta content")
    loaded = load_library(repo, _taxonomy(repo))
    assert any("duplicate id" in msg for _, msg in loaded.problems)


def test_load_detects_duplicate_bodies(repo: RepoPaths) -> None:
    """Two resources with identical bodies are flagged."""
    write_resource(repo, filename="a.md", id="ckb-aaaaaaaaaaaa", body="# Same\n\nidentical body")
    write_resource(repo, filename="b.md", id="ckb-bbbbbbbbbbbb", body="# Same\n\nidentical body")
    loaded = load_library(repo, _taxonomy(repo))
    assert any("identical body" in msg for _, msg in loaded.problems)


def test_load_skips_category_readme(repo: RepoPaths) -> None:
    """A generated category README is not loaded as a resource."""
    write_resource(repo, filename="a.md")
    (repo.library / "offensive-security" / "README.md").write_text(
        "# generated\n",
        encoding="utf-8",
    )
    loaded = load_library(repo, _taxonomy(repo))
    assert len(loaded.resources) == 1


# --- build ----------------------------------------------------------------


def test_build_generates_all_artefacts(repo: RepoPaths) -> None:
    """A build writes the catalogs and a category page."""
    write_resource(repo)
    result = build(repo, generated_at=FIXED_NOW)
    assert result.ok
    assert repo.index_json.exists()
    assert repo.index_yaml.exists()
    assert (repo.library / "offensive-security" / "README.md").exists()
    assert "offensive-security" in {name.split("/")[1] for name in result.changed if "/" in name}


def test_build_is_idempotent(repo: RepoPaths) -> None:
    """Re-building unchanged content (new timestamp only) writes nothing."""
    write_resource(repo)
    build(repo, generated_at=FIXED_NOW)
    second = build(repo)
    assert second.changed == ()


def test_build_aborts_on_problems(repo: RepoPaths) -> None:
    """A build refuses to write when the library has problems."""
    (repo.library / "stray.md").write_text("x", encoding="utf-8")
    result = build(repo)
    assert not result.ok
    assert result.problems


def test_build_without_readme(repo: RepoPaths) -> None:
    """A build creates the README when none exists."""
    repo.readme.unlink()
    write_resource(repo)
    result = build(repo, generated_at=FIXED_NOW)
    assert result.ok
    assert repo.readme.exists()


# --- checks ---------------------------------------------------------------


def test_checks_clean_repo(built_repo: RepoPaths) -> None:
    """A freshly built repository passes the policy check."""
    report = run_checks(built_repo, generated_at=FIXED_NOW)
    assert report.ok
    assert report.resource_count == 1


def test_checks_detects_drift(built_repo: RepoPaths) -> None:
    """A stale catalog file is reported as out of date."""
    built_repo.index_json.write_text('{"stale": true}\n', encoding="utf-8")
    report = run_checks(built_repo, generated_at=FIXED_NOW)
    assert not report.ok
    assert any("out of date" in f.message for f in report.errors)


def test_checks_missing_generated_file(built_repo: RepoPaths) -> None:
    """A missing catalog file is reported."""
    built_repo.index_yaml.unlink()
    report = run_checks(built_repo, generated_at=FIXED_NOW)
    assert any("missing" in f.message for f in report.errors)


def test_checks_invalid_taxonomy(repo: RepoPaths) -> None:
    """An invalid taxonomy fails the check before any resource is loaded."""
    repo.taxonomy.write_text("version: 1\n", encoding="utf-8")
    report = run_checks(repo)
    assert not report.ok
    assert report.resource_count == 0


def test_checks_restricted_license_is_error(repo: RepoPaths) -> None:
    """A restricted licence on a normal resource is an error."""
    write_resource(repo, license="LicenseRef-All-Rights-Reserved")
    build(repo, generated_at=FIXED_NOW)
    report = run_checks(repo, generated_at=FIXED_NOW)
    assert any("reference stub" in f.message for f in report.errors)


def test_checks_reference_stub_is_allowed(repo: RepoPaths) -> None:
    """A small reference stub for a restricted work is a warning, not an error."""
    write_resource(
        repo,
        license="LicenseRef-All-Rights-Reserved",
        reference_only=True,
        source_url="https://example.test/work",
        body="# Ref\n\nA short pointer to an external work, not the work itself.\n",
    )
    build(repo, generated_at=FIXED_NOW)
    report = run_checks(repo, generated_at=FIXED_NOW)
    assert report.ok
    assert any("by reference only" in f.message for f in report.warnings)


def test_checks_reference_stub_too_long_is_error(repo: RepoPaths) -> None:
    """A reference stub that exceeds the word cap is an error."""
    long_body = "# Ref\n\n" + " ".join(["word"] * (REFERENCE_STUB_MAX_WORDS + 50)) + "\n"
    write_resource(
        repo,
        license="LicenseRef-All-Rights-Reserved",
        reference_only=True,
        source_url="https://example.test/work",
        body=long_body,
    )
    build(repo, generated_at=FIXED_NOW)
    report = run_checks(repo, generated_at=FIXED_NOW)
    assert any("must stay under" in f.message for f in report.errors)


def test_checks_reference_stub_without_source_is_error(repo: RepoPaths) -> None:
    """A reference stub without a source_url is an error."""
    write_resource(
        repo,
        license="LicenseRef-All-Rights-Reserved",
        reference_only=True,
        source_url=None,
        body="# Ref\n\nA short pointer with no source link.\n",
    )
    build(repo, generated_at=FIXED_NOW)
    report = run_checks(repo, generated_at=FIXED_NOW)
    assert any("must carry a 'source_url'" in f.message for f in report.errors)


def test_checks_noassertion_is_warning(repo: RepoPaths) -> None:
    """An undetermined licence is a warning, not a gate failure."""
    write_resource(repo, license="NOASSERTION")
    build(repo, generated_at=FIXED_NOW)
    report = run_checks(repo, generated_at=FIXED_NOW)
    assert any(f.severity is Severity.WARNING for f in report.warnings)
    assert report.ok


def test_checks_active_content_is_warning(repo: RepoPaths) -> None:
    """Unfenced active content is an advisory warning, never a gate failure."""
    write_resource(
        repo,
        body="# Doc\n\nHere is <script>alert(1)</script> inline.\n",
        filename="x.md",
    )
    build(repo, generated_at=FIXED_NOW)
    report = run_checks(repo, generated_at=FIXED_NOW)
    assert any("active/executable" in f.message for f in report.warnings)
    assert report.ok


def test_checks_readme_drift(built_repo: RepoPaths) -> None:
    """A README with missing markers is reported as drift."""
    built_repo.readme.write_text("# Broken\n\nno markers\n", encoding="utf-8")
    report = run_checks(built_repo, generated_at=FIXED_NOW)
    assert any("AUTO-INDEX" in f.message or "README" in f.path for f in report.errors)


def test_checks_category_page_drift(built_repo: RepoPaths) -> None:
    """A stale category page is reported."""
    (built_repo.library / "offensive-security" / "README.md").write_text(
        "stale\n",
        encoding="utf-8",
    )
    report = run_checks(built_repo, generated_at=FIXED_NOW)
    assert any("category page" in f.message for f in report.errors)


def test_checks_missing_category_page(built_repo: RepoPaths) -> None:
    """A missing category page is reported."""
    (built_repo.library / "offensive-security" / "README.md").unlink()
    report = run_checks(built_repo, generated_at=FIXED_NOW)
    assert any("category page is missing" in f.message for f in report.errors)


def test_checks_missing_readme(built_repo: RepoPaths) -> None:
    """A missing README is reported."""
    built_repo.readme.unlink()
    report = run_checks(built_repo, generated_at=FIXED_NOW)
    assert any(f.path == "README.md" for f in report.errors)
