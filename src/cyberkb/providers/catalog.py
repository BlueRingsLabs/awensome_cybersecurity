"""The reviewed model catalog (``schema/llm-models.yaml``) and live-id resolution.

The catalog says *which* models enrichment may use, in *what* order and under
*which* free-tier limits. It never says what a model's API id is: a provider's
display name ("Gemma 4 31B") is not its id ("gemma-4-31b-it"), so every
declared model is resolved against the live ``/models`` listing by
:func:`resolve_models`, and the resolution rule is recorded so the operator can
audit exactly which id served under which name.

Loading is strict: an unknown key, a non-positive limit, a duplicated or
excluded model, or an unsupported match mode is a :class:`ModelCatalogError`,
because a silently-misread catalog would route paid-for quota to the wrong model.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, NoReturn
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import yaml

from cyberkb.errors import KBError, ModelCatalogError
from cyberkb.fsutil import read_text
from cyberkb.yamlsafe import safe_load

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping, Sequence

__all__ = [
    "CATALOG_RELPATH",
    "DeclaredModel",
    "ListedModel",
    "MatchMode",
    "ModelCatalog",
    "ModelLimits",
    "ProviderSpec",
    "Resolution",
    "load_model_catalog",
    "normalise_name",
    "parse_model_catalog",
    "resolve_models",
]

CATALOG_RELPATH = Path("schema") / "llm-models.yaml"
SUPPORTED_VERSION = 1
_MAX_CATALOG_BYTES = 200_000
_UNSTABLE_TOKENS = ("preview", "exp", "latest")
_NON_ALNUM = re.compile(r"[^a-z0-9]+")

MatchMode = Literal["display_name", "id"]
_MATCH_MODES: tuple[MatchMode, ...] = ("display_name", "id")
_TOP_KEYS = frozenset({"version", "verified_on", "source", "providers"})
_PROVIDER_KEYS = frozenset(
    {
        "id",
        "name",
        "base_url",
        "api_key_env",
        "docs",
        "match",
        "quota_timezone",
        "tpm_counts_completion",
        "exclude",
        "models",
    },
)
_MODEL_KEYS = frozenset({"name", "id_hints", "limits"})
_LIMIT_KEYS = frozenset({"rpm", "rpd", "tpm", "tpd"})
_REQUIRED_LIMITS = ("rpm", "rpd", "tpm")


def normalise_name(value: str) -> str:
    """Lower-case ``value`` and drop every non-alphanumeric character.

    ``"Gemini 3.5 Flash"`` and ``"gemini-3.5-flash"`` both become
    ``"gemini35flash"``, which is how a display name is matched to an id.
    """
    return _NON_ALNUM.sub("", value.lower())


@dataclass(frozen=True, slots=True)
class ModelLimits:
    """Free-tier limits for one model (per model; RPD resets once per quota day)."""

    rpm: int
    rpd: int
    tpm: int
    tpd: int | None = None

    def to_dict(self) -> dict[str, int | None]:
        """Serialise for the run report."""
        return {"rpm": self.rpm, "rpd": self.rpd, "tpm": self.tpm, "tpd": self.tpd}


@dataclass(frozen=True, slots=True)
class DeclaredModel:
    """A model the catalog permits, before it has been resolved to a live id."""

    provider: str
    name: str
    priority: int
    limits: ModelLimits
    id_hints: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ProviderSpec:
    """One provider block of the catalog."""

    id: str
    name: str
    base_url: str
    api_key_env: str
    docs: str
    match: MatchMode
    quota_timezone: str
    tpm_counts_completion: bool
    exclude: frozenset[str]
    models: tuple[DeclaredModel, ...]


@dataclass(frozen=True, slots=True)
class ModelCatalog:
    """The whole catalog: providers in fallback order, models in priority order."""

    version: int
    verified_on: date
    source: str
    providers: tuple[ProviderSpec, ...]

    def provider(self, provider_id: str) -> ProviderSpec:
        """Return the provider block called ``provider_id``.

        Raises:
            ModelCatalogError: no such provider is declared.
        """
        for spec in self.providers:
            if spec.id == provider_id:
                return spec
        msg = f"provider {provider_id!r} is not declared in {CATALOG_RELPATH.as_posix()}"
        raise ModelCatalogError(msg)


@dataclass(frozen=True, slots=True)
class ListedModel:
    """One entry of a provider's live ``/models`` listing, normalised."""

    id: str
    display_name: str | None = None
    input_token_limit: int | None = None
    output_token_limit: int | None = None
    shared_context: bool = False
    """``True`` when ``input_token_limit`` is a context window shared with the output."""


@dataclass(frozen=True, slots=True)
class Resolution:
    """How one declared model mapped onto the live listing (or why it did not)."""

    declared: DeclaredModel
    model: ListedModel | None
    rule: str
    alternatives: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialise for the run report's discovery section."""
        return {
            "priority": self.declared.priority,
            "provider": self.declared.provider,
            "declared_name": self.declared.name,
            "api_id": self.model.id if self.model else None,
            "api_display_name": self.model.display_name if self.model else None,
            "rule": self.rule,
            "alternatives": list(self.alternatives),
        }


def _reject(message: str, cause: BaseException | None = None) -> NoReturn:
    """Raise a :class:`ModelCatalogError` naming the catalog file."""
    msg = f"{CATALOG_RELPATH.as_posix()}: {message}"
    raise ModelCatalogError(msg) from cause


def _mapping(value: object, where: str, allowed: frozenset[str]) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        _reject(f"{where} must be a mapping")
    unknown = sorted(str(k) for k in value if k not in allowed)
    if unknown:
        _reject(f"{where} has unknown key(s): {', '.join(unknown)}")
    return value


def _text(value: object, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _reject(f"{where} must be a non-empty string")
    return value.strip()


def _positive(value: object, where: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        _reject(f"{where} must be a positive integer")
    return value


def _strings(value: object, where: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        _reject(f"{where} must be a list")
    return tuple(_text(item, f"{where}[]") for item in value)


def _limits(value: object, where: str) -> ModelLimits:
    raw = _mapping(value, where, _LIMIT_KEYS)
    for key in _REQUIRED_LIMITS:
        if key not in raw:
            _reject(f"{where} is missing {key}")
    tpd = raw.get("tpd")
    return ModelLimits(
        rpm=_positive(raw["rpm"], f"{where}.rpm"),
        rpd=_positive(raw["rpd"], f"{where}.rpd"),
        tpm=_positive(raw["tpm"], f"{where}.tpm"),
        tpd=None if tpd is None else _positive(tpd, f"{where}.tpd"),
    )


def _provider(value: object, index: int, priority: int) -> ProviderSpec:
    where = f"providers[{index}]"
    raw = _mapping(value, where, _PROVIDER_KEYS)
    provider_id = _text(raw.get("id"), f"{where}.id")
    match = raw.get("match")
    if match not in _MATCH_MODES:
        _reject(f"{where}.match must be one of {', '.join(_MATCH_MODES)}")
    counts = raw.get("tpm_counts_completion")
    if not isinstance(counts, bool):
        _reject(f"{where}.tpm_counts_completion must be a boolean")
    exclude = frozenset(_strings(raw.get("exclude"), f"{where}.exclude"))
    timezone = _text(raw.get("quota_timezone"), f"{where}.quota_timezone")
    try:
        ZoneInfo(timezone)
    except (ZoneInfoNotFoundError, ValueError) as exc:
        _reject(f"{where}.quota_timezone {timezone!r} is not a known IANA zone", exc)
    entries = raw.get("models")
    if not isinstance(entries, list) or not entries:
        _reject(f"{where}.models must be a non-empty list")
    models: list[DeclaredModel] = []
    seen: set[str] = set()
    for offset, entry in enumerate(entries):
        model_where = f"{where}.models[{offset}]"
        model_raw = _mapping(entry, model_where, _MODEL_KEYS)
        name = _text(model_raw.get("name"), f"{model_where}.name")
        if name in exclude:
            _reject(f"{model_where}: {name!r} is excluded for provider {provider_id!r}")
        if name in seen:
            _reject(f"{model_where}: {name!r} is declared twice")
        seen.add(name)
        models.append(
            DeclaredModel(
                provider=provider_id,
                name=name,
                priority=priority + offset,
                limits=_limits(model_raw.get("limits"), f"{model_where}.limits"),
                id_hints=_strings(model_raw.get("id_hints"), f"{model_where}.id_hints"),
            ),
        )
    return ProviderSpec(
        id=provider_id,
        name=_text(raw.get("name"), f"{where}.name"),
        base_url=_text(raw.get("base_url"), f"{where}.base_url").rstrip("/"),
        api_key_env=_text(raw.get("api_key_env"), f"{where}.api_key_env"),
        docs=_text(raw.get("docs"), f"{where}.docs"),
        match=match,
        quota_timezone=timezone,
        tpm_counts_completion=counts,
        exclude=exclude,
        models=tuple(models),
    )


def parse_model_catalog(data: object) -> ModelCatalog:
    """Validate a decoded catalog document and return the typed view.

    Raises:
        ModelCatalogError: on any structural or semantic problem.
    """
    raw = _mapping(data, "document", _TOP_KEYS)
    if raw.get("version") != SUPPORTED_VERSION:
        _reject(f"version must be {SUPPORTED_VERSION}")
    verified = raw.get("verified_on")
    if not isinstance(verified, date):
        _reject("verified_on must be an ISO date (YYYY-MM-DD)")
    entries = raw.get("providers")
    if not isinstance(entries, list) or not entries:
        _reject("providers must be a non-empty list")
    providers: list[ProviderSpec] = []
    priority = 1
    for index, entry in enumerate(entries):
        spec = _provider(entry, index, priority)
        if any(p.id == spec.id for p in providers):
            _reject(f"provider {spec.id!r} is declared twice")
        providers.append(spec)
        priority += len(spec.models)
    return ModelCatalog(
        version=SUPPORTED_VERSION,
        verified_on=verified,
        source=_text(raw.get("source"), "source"),
        providers=tuple(providers),
    )


def load_model_catalog(root: Path) -> ModelCatalog:
    """Read and validate ``schema/llm-models.yaml`` under ``root``.

    Raises:
        ModelCatalogError: the file is unreadable, not YAML, or invalid.
    """
    path = root / CATALOG_RELPATH
    try:
        text = read_text(path, root=root, max_bytes=_MAX_CATALOG_BYTES)
        data = safe_load(text)
    except (KBError, yaml.YAMLError) as exc:
        _reject(f"cannot load: {exc}", exc)
    return parse_model_catalog(data)


def _stability_key(model: ListedModel) -> tuple[bool, int, str]:
    unstable = any(token in model.id.lower() for token in _UNSTABLE_TOKENS)
    return (unstable, len(model.id), model.id)


def _resolve_one(
    declared: DeclaredModel,
    spec: ProviderSpec,
    listed: Sequence[ListedModel],
) -> Resolution:
    if spec.match == "id":
        exact = [m for m in listed if m.id == declared.name]
        if exact:
            return Resolution(declared, exact[0], "exact id")
        return Resolution(declared, None, "not listed by the provider")
    hinted = [m for m in listed if m.id in declared.id_hints]
    if hinted:
        hinted.sort(key=lambda m: declared.id_hints.index(m.id))
        return Resolution(declared, hinted[0], "documented id hint")
    wanted = normalise_name(declared.name)
    by_display = [m for m in listed if m.display_name and normalise_name(m.display_name) == wanted]
    by_id = [m for m in listed if normalise_name(m.id) == wanted]
    for rule, matches in (("display name", by_display), ("normalised id", by_id)):
        if matches:
            ranked = sorted(matches, key=_stability_key)
            return Resolution(declared, ranked[0], rule, tuple(m.id for m in ranked[1:]))
    return Resolution(declared, None, "not listed by the provider")


def resolve_models(spec: ProviderSpec, listed: Iterable[ListedModel]) -> list[Resolution]:
    """Map every declared model of ``spec`` onto the live listing, in priority order.

    Excluded ids are removed from the listing first, so they can never be the
    target of a match. When several live models share a display name the most
    stable one wins (no ``preview``/``exp``/``latest`` token, then the shortest
    id) and the rest are kept as ``alternatives`` for the audit trail. Two
    declared names never resolve to the same id: the later one is reported as
    a duplicate rather than double-counting a single quota.
    """
    candidates = [m for m in listed if m.id not in spec.exclude]
    resolutions: list[Resolution] = []
    taken: set[str] = set()
    for declared in spec.models:
        resolution = _resolve_one(declared, spec, candidates)
        if resolution.model is not None and resolution.model.id in taken:
            resolution = Resolution(
                declared, None, f"duplicate of an earlier declaration ({resolution.model.id})"
            )
        if resolution.model is not None:
            taken.add(resolution.model.id)
        resolutions.append(resolution)
    return resolutions
