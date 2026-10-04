"""cyberkb -- the engine behind the awesome_cybersecurity knowledge base.

The package turns raw Markdown contributions into a curated, faceted and
machine-readable library:

* :mod:`cyberkb.ingest` discovers submissions, sanitises and classifies them
  and files them under ``library/<category>/``;
* :mod:`cyberkb.catalog` builds the deterministic catalog (``index.json`` /
  ``index.yaml``) from the library;
* :mod:`cyberkb.render` generates the README index and per-category pages;
* :mod:`cyberkb.checks` enforces repository policy in CI.
"""

from __future__ import annotations

__all__ = ["__version__"]

__version__ = "2.0.0"
