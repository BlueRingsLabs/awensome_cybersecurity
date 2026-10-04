"""Hardened YAML loading for untrusted input.

``yaml.safe_load`` already refuses arbitrary object construction (CWE-502),
but it still honours anchors and aliases. A few kilobytes of nested aliases
expand into an exponentially large structure the moment it is serialised to
JSON (the "billion laughs" pattern), which would let a single contributor
front matter block exhaust the CI runner. Front matter never needs aliases,
so this loader rejects them outright.
"""

from __future__ import annotations

from typing import Any, override

import yaml

__all__ = ["YAMLAliasError", "safe_load"]


class YAMLAliasError(yaml.YAMLError):
    """Raised when a document uses anchors or aliases."""


class _NoAliasSafeLoader(yaml.SafeLoader):
    """SafeLoader that fails on the first anchor or alias it meets."""

    @override
    def compose_node(self, parent: yaml.Node | None, index: Any) -> yaml.Node | None:
        event = self.peek_event()  # type: ignore[no-untyped-call]  # PyYAML is untyped
        if isinstance(event, yaml.AliasEvent) or getattr(event, "anchor", None) is not None:
            msg = "YAML anchors and aliases are not allowed"
            raise YAMLAliasError(msg)
        return super().compose_node(parent, index)


def safe_load(text: str) -> Any:  # noqa: ANN401 -- YAML can decode to any shape
    """Parse ``text`` as YAML without object construction or aliases.

    Raises:
        yaml.YAMLError: on syntax errors; :class:`YAMLAliasError` on aliases.
    """
    loader = _NoAliasSafeLoader(text)
    try:
        return loader.get_single_data()
    finally:
        loader.dispose()
