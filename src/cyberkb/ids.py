"""Stable resource identifiers.

A catalog consumer (a dashboard, an agent, an external index) needs an id
that stays constant when a file is renamed, recategorised or lightly edited,
yet differs between genuinely different resources. v1 used
``domain.subdomain.filename`` as the id, so every move silently broke every
downstream reference.

The v2 id is ``ckb-`` followed by 12 hex digits of a BLAKE2b digest of the
document's *content signature*: its sanitised body reduced to a bag of
lowercase word tokens. Reordering sections, fixing whitespace or editing
front matter leaves the id unchanged; substantially different text produces a
different id. Collisions are detected and resolved deterministically at mint
time against the set of ids already in use.
"""

from __future__ import annotations

import hashlib

from cyberkb.textutil import tokenize

__all__ = ["ID_PREFIX", "content_signature", "mint_id"]

ID_PREFIX = "ckb-"
_ID_HEX = 12
_SIG_TOKENS = 2000


def content_signature(body: str) -> str:
    """Order-independent signature of a document body.

    The body is tokenised, the first ``_SIG_TOKENS`` tokens are kept (enough
    to distinguish any two real documents while bounding cost on large books),
    de-duplicated and sorted, so cosmetic edits do not change the signature.
    """
    tokens = sorted(set(tokenize(body)[:_SIG_TOKENS]))
    return "\n".join(tokens)


def mint_id(body: str, *, taken: frozenset[str] = frozenset()) -> str:
    """Return a stable ``ckb-<12 hex>`` id for ``body``, avoiding ids in ``taken``.

    On the astronomically unlikely digest collision with a *different*
    document, the signature is re-hashed with an incrementing salt until a
    free id is found, keeping every id unique within a build.
    """
    signature = content_signature(body).encode("utf-8")
    salt = 0
    while True:
        payload = signature if salt == 0 else signature + f"\x00{salt}".encode()
        digest = hashlib.blake2b(payload, digest_size=_ID_HEX).hexdigest()[:_ID_HEX]
        candidate = f"{ID_PREFIX}{digest}"
        if candidate not in taken:
            return candidate
        salt += 1
