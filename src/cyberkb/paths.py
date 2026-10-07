"""Repository layout constants and resolved paths.

Centralising the layout keeps every module, test and the CLI in agreement
about where things live, and makes the ``library/`` relocation from v1's
``0X_domain/subdomain`` tree a one-line change.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

__all__ = ["LIBRARY_DIRNAME", "RepoPaths"]

LIBRARY_DIRNAME = "library"
INBOX_DIRNAME = "inbox"
SCHEMA_DIRNAME = "schema"


@dataclass(frozen=True, slots=True)
class RepoPaths:
    """Resolved absolute paths for one repository checkout."""

    root: Path

    @classmethod
    def at(cls, root: Path) -> RepoPaths:
        """Resolve ``root`` to an absolute path."""
        return cls(root.resolve())

    @property
    def library(self) -> Path:
        """Directory holding the curated, categorised resources."""
        return self.root / LIBRARY_DIRNAME

    @property
    def inbox(self) -> Path:
        """Directory where contributors drop raw submissions."""
        return self.root / INBOX_DIRNAME

    @property
    def taxonomy(self) -> Path:
        """The taxonomy definition file."""
        return self.root / SCHEMA_DIRNAME / "taxonomy.yaml"

    @property
    def index_json(self) -> Path:
        """Machine-readable catalog (JSON)."""
        return self.root / "index.json"

    @property
    def index_yaml(self) -> Path:
        """Machine-readable catalog (YAML)."""
        return self.root / "index.yaml"

    @property
    def readme(self) -> Path:
        """Repository README whose index block is generated."""
        return self.root / "README.md"

    @property
    def ingest_runs(self) -> Path:
        """Directory holding dated ingestion/enrichment run reports."""
        return self.root / "docs" / "audit" / "ingest-runs"

    @property
    def enrich_state(self) -> Path:
        """The enrichment ledger (progress, per-model usage, last run)."""
        return self.root / "docs" / "audit" / "enrich-state.json"
