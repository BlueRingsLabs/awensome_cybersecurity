"""Repository policy checks run in CI and locally via ``cyberkb check``.

The check is the contract the repository promises to keep:

* the taxonomy is valid;
* every library document has valid front matter whose folder matches its
  category, a unique id and a unique body;
* no resource carries an ``all-rights-reserved`` licence (we may not
  redistribute it); an undetermined licence (``NOASSERTION``) is a warning;
* active/executable content outside code fences is flagged as a warning
  (GitHub sanitises rendered Markdown, and security notes quote payloads);
* the committed catalogs and README index are exactly what ``cyberkb build``
  would generate right now (no drift).

Each failure is a :class:`Finding` with a severity, a path and a message, so
the CLI can print them and set a non-zero exit code.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import TYPE_CHECKING

from cyberkb.catalog import build_catalog, catalog_json, catalog_yaml, strip_volatile_lines
from cyberkb.errors import KBError
from cyberkb.fsutil import read_text
from cyberkb.library import load_library
from cyberkb.licensing import Redistribution, redistribution_class
from cyberkb.markdown import active_content
from cyberkb.render import render_category_page, render_index_block, splice_readme
from cyberkb.taxonomy import load_taxonomy

if TYPE_CHECKING:
    from collections.abc import Iterable
    from datetime import datetime

    from cyberkb.library import Resource
    from cyberkb.paths import RepoPaths
    from cyberkb.taxonomy import Taxonomy

__all__ = ["CheckReport", "Finding", "Severity", "run_checks"]

_MAX_DOC_BYTES = 8 * 1024 * 1024
#: Hard cap on a reference stub's body, so restricted content cannot be smuggled in.
REFERENCE_STUB_MAX_WORDS = 400


class Severity(StrEnum):
    """Severity of a policy finding."""

    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True, slots=True)
class Finding:
    """A single policy finding."""

    severity: Severity
    path: str
    message: str


@dataclass(frozen=True, slots=True)
class CheckReport:
    """Outcome of a policy run."""

    findings: tuple[Finding, ...]
    resource_count: int

    @property
    def errors(self) -> tuple[Finding, ...]:
        """Findings at ERROR severity."""
        return tuple(f for f in self.findings if f.severity is Severity.ERROR)

    @property
    def warnings(self) -> tuple[Finding, ...]:
        """Findings at WARNING severity."""
        return tuple(f for f in self.findings if f.severity is Severity.WARNING)

    @property
    def ok(self) -> bool:
        """``True`` when there are no ERROR findings."""
        return not self.errors


def run_checks(paths: RepoPaths, *, generated_at: datetime | None = None) -> CheckReport:
    """Run every repository policy check and return the collected findings."""
    findings: list[Finding] = []
    try:
        taxonomy = load_taxonomy(paths.root)
    except KBError as exc:
        return CheckReport((Finding(Severity.ERROR, "schema/taxonomy.yaml", str(exc)),), 0)

    library = load_library(paths, taxonomy)
    findings.extend(Finding(Severity.ERROR, path, message) for path, message in library.problems)
    findings.extend(_license_findings(library.resources))
    findings.extend(_active_content_findings(paths, library.resources))
    findings.extend(_drift_findings(paths, taxonomy, library.resources, generated_at))
    findings.sort(key=lambda f: (f.severity is Severity.WARNING, f.path, f.message))
    return CheckReport(tuple(findings), len(library.resources))


def _license_findings(resources: Iterable[Resource]) -> list[Finding]:
    findings: list[Finding] = []
    for resource in resources:
        kind = redistribution_class(resource.front_matter.license)
        if kind is Redistribution.RESTRICTED:
            findings.extend(_restricted_findings(resource))
        elif resource.front_matter.license == "NOASSERTION":
            findings.append(
                Finding(
                    Severity.WARNING,
                    resource.path,
                    "licence is undetermined (NOASSERTION); confirm redistribution rights",
                ),
            )
    return findings


def _restricted_findings(resource: Resource) -> list[Finding]:
    """A redistribution-restricted work is allowed only as a small reference stub.

    Setting ``reference_only: true`` asserts the file is a maintainer-written
    pointer (title, author, source, summary) and does NOT contain the work
    itself. The word cap makes it impossible to smuggle the full text in under
    the flag, so an auditor sees we never republish restricted content.
    """
    fm = resource.front_matter
    if not fm.reference_only:
        return [
            Finding(
                Severity.ERROR,
                resource.path,
                f"licence {fm.license!r} forbids redistribution; replace the work with a "
                "reference stub (set 'reference_only: true', keep only a summary and a "
                f"source link, under {REFERENCE_STUB_MAX_WORDS} words)",
            ),
        ]
    if resource.word_count > REFERENCE_STUB_MAX_WORDS:
        return [
            Finding(
                Severity.ERROR,
                resource.path,
                f"reference stub for a restricted work must stay under "
                f"{REFERENCE_STUB_MAX_WORDS} words (has {resource.word_count}); it must not "
                "contain the work itself",
            ),
        ]
    if not fm.source_url:
        return [
            Finding(
                Severity.ERROR,
                resource.path,
                "reference stub for a restricted work must carry a 'source_url' crediting "
                "the original",
            ),
        ]
    return [
        Finding(
            Severity.WARNING,
            resource.path,
            f"included by reference only under {fm.license!r} (full work not redistributed); "
            "credited to its authors pending redistribution permission",
        ),
    ]


def _active_content_findings(paths: RepoPaths, resources: Iterable[Resource]) -> list[Finding]:
    findings: list[Finding] = []
    for resource in resources:
        try:
            text = read_text(paths.root / resource.path, root=paths.root, max_bytes=_MAX_DOC_BYTES)
        except KBError as exc:  # pragma: no cover - already read during load_library
            findings.append(Finding(Severity.ERROR, resource.path, str(exc)))
            continue
        for line_number, snippet in active_content(text):
            # Advisory, not a gate: GitHub sanitises rendered Markdown HTML, and
            # security literature legitimately quotes payloads. Flag it so a
            # maintainer can fence the snippet, but do not block the build.
            findings.append(
                Finding(
                    Severity.WARNING,
                    resource.path,
                    f"line {line_number}: active/executable content outside a code fence: "
                    f"{snippet!r}; "
                    "wrap payloads in a code block",
                ),
            )
    return findings


def _drift_findings(
    paths: RepoPaths,
    taxonomy: Taxonomy,
    resources: tuple[Resource, ...],
    generated_at: datetime | None,
) -> list[Finding]:
    """Compare committed generated files against a fresh build (ignoring the timestamp)."""
    catalog = build_catalog(resources, taxonomy, generated_at=generated_at)
    expected = {
        paths.index_json: catalog_json(catalog),
        paths.index_yaml: catalog_yaml(catalog),
    }
    block = render_index_block(catalog, resources, taxonomy)
    findings: list[Finding] = []
    for path, want in expected.items():
        rel = path.name
        try:
            have = read_text(path, root=paths.root, max_bytes=_MAX_DOC_BYTES)
        except KBError:
            findings.append(
                Finding(Severity.ERROR, rel, "generated file is missing; run `cyberkb build`")
            )
            continue
        if _strip_timestamp(have) != _strip_timestamp(want):
            findings.append(
                Finding(
                    Severity.ERROR, rel, "out of date; run `cyberkb build` and commit the result"
                )
            )

    findings.extend(_readme_drift(paths, block))
    findings.extend(_category_page_drift(paths, resources, taxonomy))
    return findings


def _readme_drift(paths: RepoPaths, block: str) -> list[Finding]:
    try:
        readme = read_text(paths.readme, root=paths.root, max_bytes=_MAX_DOC_BYTES)
    except KBError:
        return [Finding(Severity.ERROR, "README.md", "README.md is missing")]
    expected = splice_readme(readme, block)
    if _strip_timestamp(readme) != _strip_timestamp(expected):
        return [
            Finding(
                Severity.ERROR, "README.md", "AUTO-INDEX block is out of date; run `cyberkb build`"
            )
        ]
    return []


def _category_page_drift(
    paths: RepoPaths,
    resources: tuple[Resource, ...],
    taxonomy: Taxonomy,
) -> list[Finding]:
    findings: list[Finding] = []
    by_category: dict[str, list[Resource]] = {}
    for resource in resources:
        by_category.setdefault(resource.category, []).append(resource)
    for category_id, subset in by_category.items():
        page = paths.library / category_id / "README.md"
        want = render_category_page(category_id, subset, taxonomy)
        rel = f"library/{category_id}/README.md"
        try:
            have = read_text(page, root=paths.root, max_bytes=_MAX_DOC_BYTES)
        except KBError:
            findings.append(
                Finding(Severity.ERROR, rel, "category page is missing; run `cyberkb build`")
            )
            continue
        if have != want:
            findings.append(
                Finding(Severity.ERROR, rel, "category page is out of date; run `cyberkb build`")
            )
    return findings


_strip_timestamp = strip_volatile_lines
