"""Guard against drift between the bundled vref .txt and the scheme JSON.

The `*-vref.txt` files are derived artifacts of the Copenhagen scheme JSON:
`Enumerator.write_enumeration()` produces them from `versedict["maxVerses"]`.
Both are committed (the .txt for backward compatibility -- older clients fetch
them from their raw URL at runtime). This test asserts the committed .txt stay
byte-identical to what the JSON produces, so the two can never silently diverge.
"""

import pytest

from biblelib.versification.Enumerator import Enumerator
from biblelib.versification.VrefReader import VrefReader

SCOPE_KW = {
    "nt": {"nt_only": True},
    "ot": {"ot_only": True},
    "protestant": {"with_deuterocanon": False},
}


def derive_usfm(scheme: str, canon: str) -> list[str]:
    """Enumerate USFM references for a scheme/canon from the bundled JSON."""
    enumerator = Enumerator(scheme)
    refs: list[str] = []
    for book in enumerator.books(**SCOPE_KW[canon]):
        maxchapters = len(enumerator.versedict["maxVerses"][book]) + 1
        for chapter in range(1, maxchapters):
            refs.extend(enumerator.enumerate_verses(book, chapter))
    return refs


@pytest.mark.parametrize("scheme", ["eng", "org", "rso"])
@pytest.mark.parametrize("canon", ["nt", "ot", "protestant"])
def test_vref_matches_json_derivation(scheme: str, canon: str) -> None:
    """The committed vref .txt equals the JSON-derived enumeration."""
    committed = VrefReader(scheme, canon, asbcv=False).data
    assert committed == derive_usfm(scheme, canon)
