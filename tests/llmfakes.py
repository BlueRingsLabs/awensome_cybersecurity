"""Test doubles for the LLM layer, all at the HTTP boundary.

Nothing here replaces provider, engine or classifier logic: :class:`Router` is
the network (it answers HTTP requests from per-endpoint queues, so interleaved
Google and Groq calls stay deterministic), :class:`FakeTime` is the clock (a
``sleep`` advances it instantly), and the builders produce response bodies in
the documented shapes of the Gemini API and Groq's OpenAI-compatible API.
"""

from __future__ import annotations

import io
import json
import re
import urllib.parse
from datetime import UTC, date, datetime, timedelta
from typing import TYPE_CHECKING, Any

from cyberkb.classify.llm import LLMClassifier
from cyberkb.obslog import StructuredLogger
from cyberkb.pipeline import PROBE_DOCUMENT
from cyberkb.providers.catalog import CATALOG_RELPATH, parse_model_catalog
from cyberkb.providers.google import GoogleProvider
from cyberkb.providers.groq import GroqProvider
from cyberkb.providers.http import HttpResponse, HttpTransportError
from cyberkb.providers.rotation import RotationEngine, RotationSettings

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
    from pathlib import Path

    from cyberkb.providers.governor import DailyUsage
    from cyberkb.providers.rotation import CachedValidation
    from cyberkb.taxonomy import Taxonomy

    Item = HttpResponse | HttpTransportError

GOOGLE_KEY = "google-test-key-0123456789"
GROQ_KEY = "groq-test-key-0123456789"
KEYS = {"GEMINI_API_KEY": GOOGLE_KEY, "GROQ_API_KEY": GROQ_KEY}
START = datetime(2026, 10, 7, 12, 0, 0, tzinfo=UTC)

# Priority 1 and 2 are Google models, 3 is Groq: enough to exercise every
# routing path without the noise of the full production catalog.
CATALOG_DOC: dict[str, Any] = {
    "version": 1,
    "verified_on": date(2026, 10, 7),
    "source": "test fixture",
    "providers": [
        {
            "id": "google",
            "name": "Google AI Studio",
            "base_url": "https://generativelanguage.googleapis.com/v1beta",
            "api_key_env": "GEMINI_API_KEY",
            "docs": "https://ai.google.dev/gemini-api/docs",
            "match": "display_name",
            "quota_timezone": "America/Los_Angeles",
            "tpm_counts_completion": False,
            "models": [
                {
                    "name": "Gemma Test",
                    "id_hints": ["gemma-t-it"],
                    "limits": {"rpm": 30, "rpd": 100, "tpm": 100000},
                },
                {
                    "name": "Gemini Test Flash",
                    "limits": {"rpm": 10, "rpd": 50, "tpm": 250000},
                },
            ],
        },
        {
            "id": "groq",
            "name": "Groq",
            "base_url": "https://api.groq.com/openai/v1",
            "api_key_env": "GROQ_API_KEY",
            "docs": "https://console.groq.com/docs",
            "match": "id",
            "quota_timezone": "UTC",
            "tpm_counts_completion": True,
            "exclude": ["openai/gpt-oss-safeguard-20b"],
            "models": [
                {
                    "name": "groq-a",
                    "limits": {"rpm": 30, "rpd": 100, "tpm": 60000, "tpd": 1000000},
                },
            ],
        },
    ],
}

DAY = "2026-10-07"
GEMMA = "google:gemma-t-it"
FLASH = "google:gemini-test-flash"
GROQ = "groq:groq-a"


def single_model_catalog() -> dict[str, Any]:
    """The test catalog reduced to its first model (Gemma), for non-routing tests."""
    import copy  # noqa: PLC0415

    doc = copy.deepcopy(CATALOG_DOC)
    google = doc["providers"][0]
    google["models"] = google["models"][:1]
    doc["providers"] = [google]
    return doc


def catalog_yaml(doc: Mapping[str, Any] | None = None) -> str:
    """Render a catalog document as YAML (dates become ISO dates)."""
    import yaml  # noqa: PLC0415 - only the CLI/pipeline tests write a catalog file

    return yaml.safe_dump(dict(doc or CATALOG_DOC), sort_keys=False)


def write_catalog(root: Path, doc: Mapping[str, Any] | None = None) -> None:
    """Write the test catalog into ``root/schema/llm-models.yaml``."""
    target = root / CATALOG_RELPATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(catalog_yaml(doc), encoding="utf-8")


class FakeTime:
    """A deterministic clock: ``sleep`` advances time instantly and is recorded."""

    def __init__(self, start: datetime = START) -> None:
        """Start at ``start`` with no time elapsed."""
        self.t = 0.0
        self._start = start
        self.sleeps: list[float] = []

    def clock(self) -> float:
        """Monotonic seconds since the start."""
        return self.t

    def sleep(self, seconds: float) -> None:
        """Record and fast-forward."""
        self.sleeps.append(seconds)
        self.t += seconds

    def now(self) -> datetime:
        """Wall-clock time consistent with :meth:`clock`."""
        return self._start + timedelta(seconds=self.t)


class Router:
    """The network: answers each endpoint from its own queue and records calls.

    Keys are ``google:list``, ``groq:list``, ``google:<model>`` (generateContent)
    and ``groq:<model>`` (chat/completions, model read from the body). A request
    with nothing queued fails the test loudly instead of hanging or guessing.
    """

    def __init__(self) -> None:
        """Start with no queued responses."""
        self.routes: dict[str, list[Item]] = {}
        self.calls: list[tuple[str, str, dict[str, str], dict[str, Any] | None]] = []

    def add(self, key: str, *items: Item) -> Router:
        """Queue responses (or transport faults) for ``key``."""
        self.routes.setdefault(key, []).extend(items)
        return self

    def pending(self) -> dict[str, int]:
        """Queued responses not consumed yet, by key (empty when all were used)."""
        return {k: len(v) for k, v in self.routes.items() if v}

    @staticmethod
    def key(url: str, body: dict[str, Any] | None) -> str:
        """Route key for a request."""
        parsed = urllib.parse.urlsplit(url)
        provider = "google" if parsed.netloc.endswith("googleapis.com") else "groq"
        if parsed.path.endswith("/models"):
            return f"{provider}:list"
        if parsed.path.endswith(":generateContent"):
            model = parsed.path.rsplit("/", 1)[-1].split(":", 1)[0]
            return f"google:{urllib.parse.unquote(model)}"
        assert body is not None
        return f"groq:{body['model']}"

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: Mapping[str, str],
        body: bytes | None,
        timeout: float,
    ) -> HttpResponse:
        """Return (or raise) the next queued item for this request's endpoint."""
        _ = timeout
        decoded = json.loads(body) if body else None
        key = self.key(url, decoded)
        self.calls.append((method, url, dict(headers), decoded))
        queue = self.routes.get(key)
        if not queue:
            msg = f"unexpected request to {key}"
            raise AssertionError(msg)
        item = queue.pop(0)
        if isinstance(item, HttpTransportError):
            raise item
        return item

    def bodies(self, key: str) -> list[dict[str, Any]]:
        """Request bodies sent to ``key``, in order."""
        return [b for _, url, _, b in self.calls if b is not None and self.key(url, b) == key]


def http(status: int, obj: object, headers: Mapping[str, str] | None = None) -> HttpResponse:
    """An HTTP response with a JSON body."""
    return HttpResponse(status, json.dumps(obj).encode("utf-8"), dict(headers or {}))


def item(ref: str = "probe-nmap", **overrides: object) -> dict[str, Any]:
    """One valid classification answer item."""
    base: dict[str, Any] = {
        "ref": ref,
        "title": "Nmap Reconnaissance",
        "category": "offensive-security",
        "format": "guide",
        "language": "en",
        "tags": ["nmap"],
        "summary": "A practical guide to host discovery and port scanning with nmap.",
        "confidence": 0.9,
    }
    base.update(overrides)
    return base


def answer(*items: dict[str, Any]) -> dict[str, Any]:
    """A classifications payload."""
    return {"classifications": list(items) or [item()]}


def google_listing(
    *models: tuple[str, str | None], next_page: str | None = None, methods: Sequence[str] = ()
) -> HttpResponse:
    """A ``models.list`` page; ``methods`` overrides supportedGenerationMethods."""
    entries = [
        {
            "name": f"models/{mid}",
            "displayName": display,
            "inputTokenLimit": 131072,
            "outputTokenLimit": 8192,
            "supportedGenerationMethods": list(methods or ("generateContent", "countTokens")),
        }
        for mid, display in models
    ]
    page: dict[str, Any] = {"models": entries}
    if next_page:
        page["nextPageToken"] = next_page
    return http(200, page)


def default_google_listing() -> HttpResponse:
    """The listing that resolves both Google test models."""
    return google_listing(
        ("gemma-t-it", "Gemma Test IT"), ("gemini-test-flash", "Gemini Test Flash")
    )


def google_answer(
    payload: Mapping[str, Any] | str,
    *,
    finish: str | None = "STOP",
    input_tokens: int | None = 900,
    output_tokens: int | None = 60,
) -> HttpResponse:
    """A ``generateContent`` response whose text is ``payload`` (JSON-encoded if a mapping)."""
    text = payload if isinstance(payload, str) else json.dumps(payload)
    candidate: dict[str, Any] = {"content": {"parts": [{"text": text}], "role": "model"}}
    if finish is not None:
        candidate["finishReason"] = finish
    usage: dict[str, Any] = {}
    if input_tokens is not None:
        usage["promptTokenCount"] = input_tokens
    if output_tokens is not None:
        usage["candidatesTokenCount"] = output_tokens
    return http(200, {"candidates": [candidate], "usageMetadata": usage})


def google_error(
    status: int,
    rpc_status: str,
    message: str = "error",
    details: Sequence[Mapping[str, Any]] = (),
) -> HttpResponse:
    """A ``google.rpc.Status`` error response."""
    return http(
        status,
        {
            "error": {
                "code": status,
                "message": message,
                "status": rpc_status,
                "details": list(details),
            }
        },
    )


def quota_failure(*quota_ids: str, retry: str | None = None) -> list[dict[str, Any]]:
    """The ``details`` of a Gemini 429: QuotaFailure violations plus optional RetryInfo."""
    details: list[dict[str, Any]] = [
        {
            "@type": "type.googleapis.com/google.rpc.QuotaFailure",
            "violations": [
                {"quotaMetric": "generativelanguage.googleapis.com/x", "quotaId": q}
                for q in quota_ids
            ],
        },
    ]
    if retry is not None:
        details.append({"@type": "type.googleapis.com/google.rpc.RetryInfo", "retryDelay": retry})
    return details


def groq_listing(*ids: str, active: bool = True, context: int = 131072) -> HttpResponse:
    """A Groq ``/models`` response."""
    return http(
        200,
        {
            "object": "list",
            "data": [
                {"id": mid, "object": "model", "active": active, "context_window": context}
                for mid in ids
            ],
        },
    )


def groq_answer(
    payload: Mapping[str, Any] | str,
    *,
    finish: str = "stop",
    remaining: int | None = None,
    usage: Mapping[str, int] | None = None,
) -> HttpResponse:
    """A chat/completions response; ``remaining`` sets x-ratelimit-remaining-requests."""
    text = payload if isinstance(payload, str) else json.dumps(payload)
    headers = {} if remaining is None else {"x-ratelimit-remaining-requests": str(remaining)}
    return http(
        200,
        {
            "choices": [
                {"finish_reason": finish, "message": {"role": "assistant", "content": text}}
            ],
            "usage": dict(usage or {"prompt_tokens": 900, "completion_tokens": 80}),
        },
        headers,
    )


def groq_error(
    status: int, message: str, *, code: str = "", headers: Mapping[str, str] | None = None
) -> HttpResponse:
    """A Groq error response."""
    return http(
        status,
        {"error": {"message": message, "type": "invalid_request_error", "code": code}},
        headers,
    )


def discovered_router() -> Router:
    """A router with both providers' listings queued."""
    return (
        Router()
        .add("google:list", default_google_listing())
        .add("groq:list", groq_listing("groq-a"))
    )


def make_engine(
    router: Router,
    *,
    settings: RotationSettings | None = None,
    clock: FakeTime | None = None,
    usage: Mapping[str, DailyUsage] | None = None,
    validations: Mapping[str, CachedValidation] | None = None,
    catalog_doc: Mapping[str, Any] | None = None,
) -> tuple[RotationEngine, FakeTime]:
    """An engine over both test providers, wired to ``router`` and a fake clock."""
    time = clock or FakeTime()
    catalog = parse_model_catalog(dict(catalog_doc or CATALOG_DOC))
    providers = [
        GoogleProvider(GOOGLE_KEY, transport=router, clock=time.clock),
        GroqProvider(GROQ_KEY, transport=router, clock=time.clock),
    ]
    engine = RotationEngine(
        providers,
        catalog,
        settings=settings or RotationSettings(list_backoff=30.0),
        logger=StructuredLogger(io.StringIO(), now=time.now),
        clock=time.clock,
        sleep=time.sleep,
        jitter=lambda: 0.5,
        now=time.now,
        usage=usage,
        validations=validations,
    )
    return engine, time


def make_classifier(
    router: Router,
    taxonomy: Taxonomy,
    **kwargs: Any,  # noqa: ANN401 - forwarded to make_engine
) -> tuple[LLMClassifier, FakeTime]:
    """A discovered classifier (probe = the production probe document)."""
    engine, time = make_engine(router, **kwargs)
    classifier = LLMClassifier(engine, taxonomy)
    engine.discover(classifier.request([PROBE_DOCUMENT], single=True))
    return classifier, time


def validated_today(*keys: str, mode: str = "json_schema") -> dict[str, CachedValidation]:
    """Validation verdicts for today (the test day), so tests skip the probe call."""
    from cyberkb.providers.rotation import CachedValidation  # noqa: PLC0415

    return {
        key: CachedValidation(DAY, ok=True, mode=mode, category=None, detail="")
        for key in (keys or (GEMMA, FLASH, GROQ))
    }


def probe_ok() -> HttpResponse:
    """A Google answer that passes validation."""
    return google_answer(answer(item("probe-nmap")))


class EchoNetwork:
    """A network that answers every classification with valid items for the prompt's refs.

    Used for end-to-end CLI runs where the number of calls is incidental.
    ``google``/``groq`` select the behaviour per provider: ``"ok"``, ``"daily"``
    (a per-day quota 429) or ``"error"`` (a 500).
    """

    _REF_RE = re.compile(r'ref=\\?"([^"\\]+)')

    def __init__(self, *, google: str = "ok", groq: str = "ok") -> None:
        """Choose each provider's behaviour."""
        self.behaviour = {"google": google, "groq": groq}
        self.calls: list[str] = []

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: Mapping[str, str],
        body: bytes | None,
        timeout: float,
    ) -> HttpResponse:
        """Answer listings and classification calls."""
        _ = (method, headers, timeout)
        decoded = json.loads(body) if body else None
        key = Router.key(url, decoded)
        self.calls.append(key)
        if key == "google:list":
            return default_google_listing()
        if key == "groq:list":
            return groq_listing("groq-a")
        provider = key.split(":", 1)[0]
        mode = self.behaviour[provider]
        if mode == "daily":
            if provider == "google":
                return google_error(429, "RESOURCE_EXHAUSTED", "q", quota_failure("PerDayQuota"))
            return groq_error(429, "Limit reached on requests per day (RPD)")
        if mode == "error":
            return http(500, {"error": {"message": "boom", "status": "INTERNAL"}})
        refs = self._REF_RE.findall(json.dumps(decoded)) or ["probe-nmap"]
        payload = answer(*(item(ref) for ref in refs))
        return google_answer(payload) if provider == "google" else groq_answer(payload)
