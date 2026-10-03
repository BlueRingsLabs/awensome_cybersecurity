#!/usr/bin/env python3
"""
generate_catalog.py — Standalone catalog regeneration utility (Issue #6 tooling).

Rebuilds index.json, index.yaml and the README.md AUTO-INDEX block from the current
repository tree, without touching root submissions or calling any AI service.

Usage:
    python3 .github/scripts/generate_catalog.py [--check] [--repo-root PATH]

Exit codes:
    0  catalogs written (or verified up-to-date with --check)
    1  (--check only) catalogs are stale / drift detected — CI can gate on this
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import catalog_lib as lib


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate repository catalogs.")
    parser.add_argument("--check", action="store_true",
                        help="do not write; exit 1 if generated output would differ")
    parser.add_argument("--repo-root", default=None, help="override repo root path")
    parser.add_argument("--fresh-timestamp", action="store_true",
                        help="force generated_at to now instead of reusing the existing stamp")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve() if args.repo_root else lib.REPO_ROOT
    from datetime import datetime
    catalog = lib.build_catalog(root, generated_at=(
        datetime.now(lib._TZ).isoformat(timespec="seconds") if args.fresh_timestamp else None))
    stats = catalog["stats"]
    print(f"📦 Catalog: {stats['total_resources']} resources "
          f"({', '.join(f'{k}={v}' for k, v in stats['by_domain'].items())})")

    if args.check:
        expected_json = lib.render_json(catalog)
        expected_yaml = lib.render_yaml(catalog)
        drift = []
        j = root / "index.json"
        y = root / "index.yaml"
        if not j.exists() or j.read_text(encoding="utf-8") != expected_json:
            drift.append("index.json")
        if not y.exists() or y.read_text(encoding="utf-8") != expected_yaml:
            drift.append("index.yaml")
        readme = root / "README.md"
        if readme.exists():
            txt = readme.read_text(encoding="utf-8")
            if lib.render_readme_table(catalog).split("\n", 1)[0] not in txt:
                pass  # header line always matches; deep check below via marker round-trip
            probe = readme.with_suffix(".md.probe")
            probe.write_text(txt, encoding="utf-8")
            lib.inject_into_readme(lib.render_readme_table(catalog), probe)
            if probe.read_text(encoding="utf-8") != txt:
                drift.append("README.md")
            probe.unlink()
        if drift:
            print("❌ Catalog drift detected:", ", ".join(drift))
            return 1
        print("✅ Catalogs are up to date.")
        return 0

    changed = lib.write_catalogs(catalog, root)
    for name, flag in changed.items():
        print(f"   {'✏️ ' if flag else '➖ '} {name}{'updated' if flag else 'unchanged'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
