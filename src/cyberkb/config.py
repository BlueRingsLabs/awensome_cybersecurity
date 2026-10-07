"""Runtime configuration from environment variables.

Which providers and models exist, in what order and under which limits is not
configuration but reviewed data (``schema/llm-models.yaml``, ADR-0008). This
module only resolves the operational knobs, each with a documented default and
a hard range. A value that is not an integer or falls outside its range is a
:class:`ConfigError` — a typo in a workflow variable must stop the run, not be
quietly replaced by a default.

=========================  =======  ==========  ===============================
Variable                   Default  Range       Meaning
=========================  =======  ==========  ===============================
``CYBERKB_BATCH_SIZE``     10       1–50        inbox documents per LLM request
``CYBERKB_TIMEOUT``        60       5–300       seconds per HTTP request
``CYBERKB_MODEL_RETRIES``  3        0–10        same-model retries after an error
``CYBERKB_LIST_PASSES``    2        1–5         walks of the whole model list
``CYBERKB_LIST_BACKOFF``   60       0–900       seconds before re-walking the list
=========================  =======  ==========  ===============================
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING

from cyberkb.errors import KBError
from cyberkb.providers.rotation import RotationSettings

if TYPE_CHECKING:
    from collections.abc import Mapping

__all__ = ["ConfigError", "IngestConfig"]


class ConfigError(KBError):
    """An operational setting is malformed or out of range."""


def _int(env: Mapping[str, str], key: str, default: int, low: int, high: int) -> int:
    raw = (env.get(key) or "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        msg = f"{key}={raw!r} is not an integer"
        raise ConfigError(msg) from exc
    if not low <= value <= high:
        msg = f"{key}={value} is outside the allowed range {low}..{high}"
        raise ConfigError(msg)
    return value


@dataclass(frozen=True, slots=True)
class IngestConfig:
    """Resolved operational configuration."""

    batch_size: int
    timeout: float
    rotation: RotationSettings

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> IngestConfig:
        """Build configuration from ``env`` (defaults to :data:`os.environ`).

        Raises:
            ConfigError: a variable is malformed or out of range.
        """
        env = os.environ if env is None else env
        rotation = RotationSettings(
            model_retries=_int(env, "CYBERKB_MODEL_RETRIES", 3, 0, 10),
            list_passes=_int(env, "CYBERKB_LIST_PASSES", 2, 1, 5),
            list_backoff=float(_int(env, "CYBERKB_LIST_BACKOFF", 60, 0, 900)),
        )
        return cls(
            batch_size=_int(env, "CYBERKB_BATCH_SIZE", 10, 1, 50),
            timeout=float(_int(env, "CYBERKB_TIMEOUT", 60, 5, 300)),
            rotation=rotation,
        )
