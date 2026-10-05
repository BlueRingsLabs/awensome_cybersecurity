"""Tests for id minting, language detection and licence detection."""

from __future__ import annotations

import pytest

from cyberkb.ids import ID_PREFIX, content_signature, mint_id
from cyberkb.language import detect_language
from cyberkb.licensing import Redistribution, detect_license, redistribution_class

# Representative samples long enough to clear the language detector's confidence
# floor, kept as named constants so the parametrize table stays readable.
_EN_SAMPLE = (
    "The quick brown fox jumps over the lazy dog and the cat while we are using this for a test"
)
_ES_SAMPLE = (
    "La seguridad es muy importante por eso los sistemas con sus usuarios no pueden estar sin "
    "control desde el principio y las empresas tienen que proteger sus datos con mucho cuidado "
    "porque los ataques son cada vez mas frecuentes en todas las redes"
)
_PT_SAMPLE = (
    "A seguranca e muito importante por isso os sistemas com voce nao podem estar sem um bom "
    "controle desde o inicio e as empresas tem que proteger os seus dados com muito cuidado "
    "porque os ataques sao cada vez mais frequentes em todas as redes"
)


def test_mint_id_shape() -> None:
    """A minted id has the 'ckb-' prefix and twelve hex digits."""
    ident = mint_id("some body text about security")
    assert ident.startswith(ID_PREFIX)
    assert len(ident) == len(ID_PREFIX) + 12


def test_mint_id_stable_under_reorder() -> None:
    """Reordering the same words yields the same id (order-independent signature)."""
    a = mint_id("alpha beta gamma delta")
    b = mint_id("delta gamma beta alpha")
    assert a == b


def test_mint_id_differs_for_different_content() -> None:
    """Different content yields different ids."""
    assert mint_id("completely different words here") != mint_id("another distinct body entirely")


def test_mint_id_avoids_collision() -> None:
    """A requested id already in use is salted to a fresh, distinct id."""
    first = mint_id("shared content tokens")
    second = mint_id("shared content tokens", taken=frozenset({first}))
    assert second != first
    assert second.startswith(ID_PREFIX)


def test_content_signature_dedupes_and_sorts() -> None:
    """The content signature is the sorted, de-duplicated token set."""
    sig = content_signature("b a b a")
    assert sig == "a\nb"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (_EN_SAMPLE, "en"),
        (_ES_SAMPLE, "es"),
        (_PT_SAMPLE, "pt"),
        ("xyzzy", "und"),
        ("", "und"),
    ],
)
def test_detect_language(text: str, expected: str) -> None:
    """English, Spanish and Portuguese are distinguished; weak input is 'und'."""
    assert detect_language(text) == expected


@pytest.mark.parametrize(
    ("snippet", "expected_license", "expected_class"),
    [
        (
            "This work is licensed under a Creative Commons Attribution 4.0 International License.",
            "CC-BY-4.0",
            Redistribution.PERMITTED,
        ),
        (
            "licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 Intl",
            "CC-BY-NC-SA-4.0",
            Redistribution.NONCOMMERCIAL,
        ),
        (
            "see http://creativecommons.org/licenses/by-sa/3.0/ for terms",
            "CC-BY-SA-3.0",
            Redistribution.PERMITTED,
        ),
        (
            "distributed under http://creativecommons.org/publicdomain/zero/1.0/ terms",
            "CC0-1.0",
            Redistribution.PERMITTED,
        ),
        (
            "This information is licensed under the Open Government Licence v3.0.",
            "OGL-UK-3.0",
            Redistribution.PERMITTED,
        ),
        (
            (
                "permission to copy under the terms of the GNU Free Documentation License, "
                "Version 1.3 or any later"
            ),
            "GFDL-1.3-or-later",
            Redistribution.PERMITTED,
        ),
        (
            "This document is herewith granted to the Public Domain. No copyright!",
            "LicenseRef-Public-Domain",
            Redistribution.PERMITTED,
        ),
        (
            "Copyright 2013 Example Corp. All rights reserved.",
            "LicenseRef-All-Rights-Reserved",
            Redistribution.RESTRICTED,
        ),
        ("just some ordinary text with no licence", "NOASSERTION", Redistribution.UNKNOWN),
    ],
)
def test_detect_license(
    snippet: str,
    expected_license: str,
    expected_class: Redistribution,
) -> None:
    """Each licence form maps to the right SPDX id and redistribution class."""
    finding = detect_license(snippet)
    assert finding.license == expected_license
    assert redistribution_class(finding.license) is expected_class


def test_license_grant_beats_all_rights_reserved() -> None:
    """An open grant wins over an embedded 'all rights reserved' notice."""
    text = (
        "Chapter 1. Some text about security. "
        "This book is licensed under a Creative Commons Attribution 4.0 International License. "
        "Embedded video content is All rights reserved by its owners."
    )
    assert detect_license(text).license == "CC-BY-4.0"


def test_bare_cc_abbreviation_requires_grant_context() -> None:
    """A CC abbreviation counts only with a grant phrase, not as a passing mention."""
    with_grant = "We used Mimikatz, which is released under CC BY-NC-SA 4.0, during the test."
    passing_mention = "The tool bundles data (CC BY-NC-SA 4.0) from another project."
    assert detect_license(with_grant).license == "CC-BY-NC-SA-4.0"
    assert detect_license(passing_mention).license == "NOASSERTION"


def test_license_evidence_is_captured() -> None:
    """A detected licence carries the surrounding evidence text."""
    finding = detect_license(
        "This work is licensed under the Creative Commons Attribution 4.0 license",
    )
    assert "Creative Commons" in finding.evidence


def test_ogl_version_default() -> None:
    """An unversioned Open Government Licence defaults to v3.0."""
    assert detect_license("published under the Open Government Licence").license == "OGL-UK-3.0"


def test_redistribution_permissive_prefixes() -> None:
    """Permissive licence families map to PERMITTED; unknown ids map to UNKNOWN."""
    assert redistribution_class("MIT") is Redistribution.PERMITTED
    assert redistribution_class("Apache-2.0") is Redistribution.PERMITTED
    assert redistribution_class("BSD-3-Clause") is Redistribution.PERMITTED
    assert redistribution_class("Weird-1.0") is Redistribution.UNKNOWN


def test_cc_by_nd_text_form() -> None:
    """A spelled-out Attribution-NoDerivatives grant maps to CC-BY-ND."""
    text = (
        "This work is licensed under a Creative Commons Attribution-NoDerivatives 4.0 "
        "International License."
    )
    assert detect_license(text).license == "CC-BY-ND-4.0"
