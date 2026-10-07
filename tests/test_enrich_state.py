"""Tests for the enrichment ledger: persistence, reconciliation, move recovery."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest

from cyberkb.enrich_state import (
    EnrichState,
    InFlightMove,
    ResourceState,
    StateError,
    load_state,
    reconcile,
    recover,
    save_state,
)
from cyberkb.frontmatter import Classification
from cyberkb.library import load_library
from cyberkb.providers.governor import DailyUsage
from cyberkb.providers.rotation import CachedValidation
from cyberkb.taxonomy import load_taxonomy
from tests.conftest import write_resource

if TYPE_CHECKING:
    from cyberkb.paths import RepoPaths

NOW = "2026-10-07T12:00:00Z"
HEURISTIC = Classification("heuristic", 0.4)


def test_missing_ledger_is_empty(repo: RepoPaths) -> None:
    """No ledger yet means a fresh, empty state."""
    state = load_state(repo)
    assert state.resources == {}
    assert state.counts() == {"pending": 0, "enriched": 0, "failed": 0}


def test_round_trip_preserves_everything(repo: RepoPaths) -> None:
    """Resources, usage, validations, last run and an in-flight move survive a save."""
    state = EnrichState(
        resources={
            "ckb-1": ResourceState(
                "failed",
                "library/a/x.md",
                attempts=2,
                last_error_category="content_filter",
                last_error="blocked",
            ),
            "ckb-2": ResourceState(
                "enriched",
                "library/a/y.md",
                provider="google",
                model="gemma-4-31b-it",
                updated_at=NOW,
            ),
        },
        usage={"google:gemma-4-31b-it": DailyUsage("2026-10-07", 3, 900)},
        validations={
            "groq:groq-a": CachedValidation(
                "2026-10-07", ok=False, mode=None, category="model_unavailable", detail="gone"
            )
        },
        last_run={"run_id": "gh1-1", "status": "partial"},
        in_flight=InFlightMove("ckb-1", "library/a/x.md", "library/b/x.md"),
    )
    path = save_state(repo, state, now_iso=NOW)
    assert path == repo.enrich_state
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["summary"] == {"pending": 0, "enriched": 1, "failed": 1}
    loaded = load_state(repo)
    assert loaded.resources["ckb-1"].last_error_category == "content_filter"
    assert loaded.resources["ckb-2"].model == "gemma-4-31b-it"
    assert loaded.usage["google:gemma-4-31b-it"].tokens == 900
    assert loaded.validations["groq:groq-a"].detail == "gone"
    assert "groq:groq-a" not in loaded.usage
    assert loaded.last_run == {"run_id": "gh1-1", "status": "partial"}
    assert loaded.in_flight == InFlightMove("ckb-1", "library/a/x.md", "library/b/x.md")
    assert loaded.updated_at == NOW


@pytest.mark.parametrize(
    ("content", "message"),
    [
        ("{not json", "invalid JSON"),
        ('{"schema_version": 99}', "schema_version"),
        ('{"schema_version": 1, "resources": []}', "must be objects"),
        ('{"schema_version": 1, "resources": {"x": {"status": "odd"}}}', "no valid status"),
        ('{"schema_version": 1, "resources": {"x": {"status": "pending"}}}', "no path"),
        ('{"schema_version": 1, "models": {"m": 1}}', "is not an object"),
        ('{"schema_version": 1, "in_flight": {"resource_id": "x"}}', "complete move record"),
    ],
)
def test_a_broken_ledger_is_an_error_not_a_fresh_start(
    repo: RepoPaths, content: str, message: str
) -> None:
    """Silently restarting would re-spend quota on finished work."""
    repo.enrich_state.parent.mkdir(parents=True, exist_ok=True)
    repo.enrich_state.write_text(content, encoding="utf-8")
    with pytest.raises(StateError, match=message):
        load_state(repo)


def test_lenient_optional_fields(repo: RepoPaths) -> None:
    """Odd optional values degrade to defaults; malformed usage entries are dropped."""
    repo.enrich_state.parent.mkdir(parents=True, exist_ok=True)
    repo.enrich_state.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "last_run": "x",
                "resources": {
                    "x": {"status": "pending", "path": "p", "attempts": -4, "provider": 7}
                },
                "models": {"m": {"usage": {"requests": 2}, "validation": "nope"}},
            },
        ),
        encoding="utf-8",
    )
    state = load_state(repo)
    assert state.resources["x"].attempts == 0
    assert state.resources["x"].provider is None
    assert state.usage == {}
    assert state.validations == {}
    assert state.last_run is None


def test_reconcile_follows_the_front_matter(repo: RepoPaths) -> None:
    """LLM → enriched, heuristic → pending (or still failed), manual → out of scope."""
    write_resource(repo, filename="a.md", id="ckb-00000000000a", classification=HEURISTIC)
    write_resource(
        repo,
        filename="b.md",
        id="ckb-00000000000b",
        classification=Classification("llm", 0.9, "gemma-4-31b-it"),
        classified_by="google:gemma-4-31b-it@2026-10-07T10:00:00Z",
    )
    write_resource(repo, filename="c.md", id="ckb-00000000000c", classification=HEURISTIC)
    write_resource(repo, filename="d.md", id="ckb-00000000000d")
    write_resource(
        repo,
        filename="e.md",
        id="ckb-00000000000e",
        classification=Classification("llm", 0.9, "m"),
        classified_by="llm@2026-10-07T10:00:00Z",
    )
    state = EnrichState(
        resources={
            "ckb-00000000000c": ResourceState(
                "failed", "old", attempts=1, last_error_category="content_filter", last_error="x"
            ),
            "ckb-gone": ResourceState("pending", "library/x/gone.md"),
        },
    )
    library = load_library(repo, load_taxonomy(repo.root))
    reconcile(state, library)
    assert state.resources["ckb-00000000000a"].status == "pending"
    enriched = state.resources["ckb-00000000000b"]
    assert (enriched.status, enriched.provider, enriched.model) == (
        "enriched",
        "google",
        "gemma-4-31b-it",
    )
    failed = state.resources["ckb-00000000000c"]
    assert (failed.status, failed.attempts, failed.last_error) == ("failed", 1, "x")
    assert failed.path == "library/offensive-security/c.md"
    assert "ckb-00000000000d" not in state.resources
    assert "ckb-gone" not in state.resources
    assert state.resources["ckb-00000000000e"].provider is None
    reconcile(state, library, force=True)
    assert state.resources["ckb-00000000000b"].status == "pending"


def _two_copies(
    repo: RepoPaths, *, ids: tuple[str, str] = ("ckb-000000000001", "ckb-000000000001")
) -> EnrichState:
    write_resource(repo, filename="old.md", id=ids[0])
    write_resource(repo, category="incident-response-and-forensics", filename="new.md", id=ids[1])
    return EnrichState(
        in_flight=InFlightMove(
            "ckb-000000000001",
            "library/offensive-security/old.md",
            "library/incident-response-and-forensics/new.md",
        ),
    )


def test_recover_completes_a_half_done_move(repo: RepoPaths) -> None:
    """Both copies present: the source is removed and the record cleared."""
    state = _two_copies(repo)
    note = recover(repo, state)
    assert note is not None
    assert "removed library/offensive-security/old.md" in note
    assert not (repo.library / "offensive-security" / "old.md").exists()
    assert state.in_flight is None


def test_recover_leaves_mismatched_files_alone(repo: RepoPaths) -> None:
    """If the two files are not the same resource, nothing is deleted."""
    state = _two_copies(repo, ids=("ckb-000000000001", "ckb-000000000002"))
    note = recover(repo, state)
    assert note is not None
    assert "ids do not match" in note
    assert (repo.library / "offensive-security" / "old.md").exists()


def test_recover_when_the_move_finished_or_never_landed(repo: RepoPaths) -> None:
    """Destination only → done; source only → nothing to undo; none → no-op."""
    assert recover(repo, EnrichState()) is None
    write_resource(repo, category="incident-response-and-forensics", filename="new.md")
    done = EnrichState(
        in_flight=InFlightMove(
            "ckb-000000000001",
            "library/offensive-security/old.md",
            "library/incident-response-and-forensics/new.md",
        )
    )
    assert "already completed" in (recover(repo, done) or "")
    write_resource(repo, filename="src.md")
    never = EnrichState(
        in_flight=InFlightMove(
            "ckb-000000000001",
            "library/offensive-security/src.md",
            "library/incident-response-and-forensics/missing.md",
        )
    )
    assert "never landed" in (recover(repo, never) or "")
    assert (repo.library / "offensive-security" / "src.md").exists()


def test_recover_ignores_unreadable_front_matter(repo: RepoPaths) -> None:
    """A destination that cannot be read is treated as a different resource."""
    state = _two_copies(repo)
    (repo.library / "incident-response-and-forensics" / "new.md").write_bytes(b"\x00binary")
    assert "ids do not match" in (recover(repo, state) or "")


@pytest.mark.parametrize(
    ("source", "destination", "message"),
    [
        ("README.md", "library/a/x.md", "not a library document"),
        ("library/a/x.md", "library/a/x.txt", "not a library document"),
        ("../outside.md", "library/a/x.md", "unsafe"),
    ],
)
def test_recover_refuses_paths_outside_the_library(
    repo: RepoPaths, source: str, destination: str, message: str
) -> None:
    """A tampered ledger can never make recovery delete an arbitrary file."""
    state = EnrichState(in_flight=InFlightMove("ckb-000000000001", source, destination))
    with pytest.raises(StateError, match=message):
        recover(repo, state)
    assert repo.readme.exists()
