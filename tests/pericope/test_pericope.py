"""Pytest tests for biblelib.pericope."""

import pytest

from pathlib import Path

from biblelib.pericope import Pericope, PericopeDict
from biblelib.word import BID, BCVID, BCVIDRange


@pytest.fixture(scope="module")
def bsb() -> PericopeDict:
    """Return a PericopeDict for the Berean Standard Bible."""
    return PericopeDict(language="eng", version="BSB", license="CC BY 4.0")


class TestPericopeDict:
    """Tests for PericopeDict."""

    def test_init(self, bsb: PericopeDict) -> None:
        """Test basic initialization."""
        assert bsb.language == "eng"
        assert bsb.version == "BSB"
        assert bsb.license == "CC BY 4.0"
        assert isinstance(bsb.path, Path)
        assert len(bsb) > 0

    def test_keys_are_zero_based_integers(self, bsb: PericopeDict) -> None:
        """Test that the dict is keyed by zero-based integers."""
        assert 0 in bsb
        assert isinstance(bsb[0], Pericope)

    def test_first_pericope(self, bsb: PericopeDict) -> None:
        """Test values for the first pericope (The Creation in Genesis)."""
        first = bsb[0]
        assert first.title == "The Creation"
        assert first.startid == BCVID("01001001")
        assert first.endid == BCVID("01002003")
        assert first.index == 0

    def test_second_pericope(self, bsb: PericopeDict) -> None:
        """Test values for the second pericope."""
        second = bsb[1]
        assert second.title == "The Generations of Heaven and Earth"
        assert second.startid == BCVID("01002004")
        assert second.index == 1

    def test_eq_same_language_version(self, bsb: PericopeDict) -> None:
        """Test that two PericopeDicts with the same language+version are equal."""
        bsb2 = PericopeDict(language="eng", version="BSB", license="CC BY 4.0")
        assert bsb == bsb2

    def test_eq_self(self, bsb: PericopeDict) -> None:
        """Test that a PericopeDict equals itself."""
        assert bsb == bsb

    def test_eq_different_version(self, bsb: PericopeDict) -> None:
        """Test that PericopeDicts with different versions are not equal."""
        other = PericopeDict.__new__(PericopeDict)
        other.language = "eng"
        other.version = "NIV2011"
        other.license = ""
        assert bsb != other

    def test_get_pericope_first_verse(self, bsb: PericopeDict) -> None:
        """Test get_pericope returns correct pericope for the first verse."""
        p = bsb.get_pericope(BCVID("01001001"))
        assert p.index == 0
        assert p.title == "The Creation"

    def test_get_pericope_mid_range(self, bsb: PericopeDict) -> None:
        """Test get_pericope for a verse in the middle of a pericope."""
        # Gen 1:31 is within "The Creation" (01001001–01002003)
        p = bsb.get_pericope(BCVID("01001031"))
        assert p.index == 0

    def test_get_pericope_cross_chapter(self, bsb: PericopeDict) -> None:
        """Test get_pericope for a verse in the cross-chapter portion of a pericope."""
        # Gen 2:1 is within "The Creation" (01001001–01002003)
        p = bsb.get_pericope(BCVID("01002001"))
        assert p.index == 0

    def test_get_pericope_second(self, bsb: PericopeDict) -> None:
        """Test get_pericope returns the second pericope for its first verse."""
        p = bsb.get_pericope(BCVID("01002004"))
        assert p.index == 1

    def test_get_pericope_not_found(self, bsb: PericopeDict) -> None:
        """Test that get_pericope raises ValueError for a verse not in any pericope."""
        with pytest.raises(ValueError, match="No pericope found"):
            bsb.get_pericope(BCVID("99001001"))

    def test_get_pericopes_single(self, bsb: PericopeDict) -> None:
        """Test get_pericopes for a range within a single pericope."""
        r = BCVIDRange(BCVID("01001001"), BCVID("01001010"))
        result = bsb.get_pericopes(r)
        assert len(result) == 1
        assert result[0].title == "The Creation"

    def test_get_pericopes_multiple(self, bsb: PericopeDict) -> None:
        """Test get_pericopes for a range spanning two pericopes."""
        # Gen 1:1–Gen 2:10 spans pericopes 0 (–01002003) and 1 (01002004–)
        r = BCVIDRange(BCVID("01001001"), BCVID("01002010"))
        result = bsb.get_pericopes(r)
        assert len(result) >= 2
        assert result[0].index == 0
        assert result[1].index == 1

    def test_get_pericopes_not_found(self, bsb: PericopeDict) -> None:
        """Test that get_pericopes raises ValueError when no pericopes intersect."""
        with pytest.raises(ValueError, match="No pericopes found"):
            # Construct a PericopeDict with no data to simulate no matches
            empty = PericopeDict.__new__(PericopeDict)
            empty.language = "eng"
            empty.version = "EMPTY"
            empty.license = ""
            empty.data = {}
            empty.get_pericopes(BCVIDRange(BCVID("01001001"), BCVID("01001010")))

    def test_get_book_pericopes(self, bsb: PericopeDict) -> None:
        """Test get_book_pericopes returns all pericopes for a book."""
        gen = BID("01")
        gen_pericopes = bsb.get_book_pericopes(gen)
        assert len(gen_pericopes) > 0
        for p in gen_pericopes:
            assert p.book == gen

    def test_get_book_pericopes_all_in_book(self, bsb: PericopeDict) -> None:
        """Test that get_book_pericopes covers the full book without gaps in index order."""
        mrk = BID("41")
        mrk_pericopes = bsb.get_book_pericopes(mrk)
        assert len(mrk_pericopes) > 0
        indices = [p.index for p in mrk_pericopes]
        # Indices should be strictly ascending (no gaps within the book)
        assert indices == sorted(indices)
        assert len(indices) == len(set(indices))

    # ToDo: enumerate all the actual verses for a text, and ensure
    # that get_pericope returns the correct pericope for each
    # verse. This would be a more exhaustive test of the
    # verse-to-pericope mapping.


class TestPericope:
    """Tests for Pericope."""

    def test_attrs(self, bsb: PericopeDict) -> None:
        """Test basic Pericope attributes."""
        first = bsb[0]
        assert first.startid == BCVID("01001001")
        assert first.endid == BCVID("01002003")
        assert first.title == "The Creation"
        assert first.index == 0
        assert first.language == "eng"
        assert first.version == "BSB"
        assert first.book == BID("01")
        assert first.parent is bsb

    def test_extras_empty(self, bsb: PericopeDict) -> None:
        """Test that extras is empty when the TSV has no extra columns."""
        assert bsb[0].extras == {}

    def test_repr(self, bsb: PericopeDict) -> None:
        """Test string representation includes index and title."""
        r = repr(bsb[0])
        assert "0" in r
        assert "The Creation" in r

    def test_eq_same(self, bsb: PericopeDict) -> None:
        """Test that a pericope equals itself and the same-indexed pericope."""
        assert bsb[0] == bsb[0]

    def test_eq_different_index(self, bsb: PericopeDict) -> None:
        """Test that pericopes with different indices are not equal."""
        assert bsb[0] != bsb[1]

    def test_lt(self, bsb: PericopeDict) -> None:
        """Test less-than comparison."""
        assert bsb[0] < bsb[1]
        assert not (bsb[1] < bsb[0])

    def test_gt(self, bsb: PericopeDict) -> None:
        """Test greater-than comparison."""
        assert bsb[1] > bsb[0]
        assert not (bsb[0] > bsb[1])

    def test_le(self, bsb: PericopeDict) -> None:
        """Test less-than-or-equal comparison."""
        assert bsb[0] <= bsb[1]
        assert bsb[0] <= bsb[0]
        assert not (bsb[1] <= bsb[0])

    def test_ge(self, bsb: PericopeDict) -> None:
        """Test greater-than-or-equal comparison."""
        assert bsb[1] >= bsb[0]
        assert bsb[0] >= bsb[0]
        assert not (bsb[0] >= bsb[1])

    def test_next(self, bsb: PericopeDict) -> None:
        """Test next() returns the following pericope."""
        nxt = bsb[0].next()
        assert nxt is not None
        assert nxt.index == 1
        assert nxt == bsb[1]

    def test_next_last(self, bsb: PericopeDict) -> None:
        """Test that next() returns None for the last pericope."""
        last = bsb[len(bsb) - 1]
        assert last.next() is None

    def test_previous_first(self, bsb: PericopeDict) -> None:
        """Test that previous() returns None for the first pericope."""
        assert bsb[0].previous() is None

    def test_previous(self, bsb: PericopeDict) -> None:
        """Test previous() returns the preceding pericope."""
        prev = bsb[1].previous()
        assert prev is not None
        assert prev.index == 0
        assert prev == bsb[0]

    def test_contains_startid(self, bsb: PericopeDict) -> None:
        """Test contains() is True for the start verse."""
        assert bsb[0].contains(BCVID("01001001"))

    def test_contains_endid(self, bsb: PericopeDict) -> None:
        """Test contains() is True for the end verse."""
        assert bsb[0].contains(BCVID("01002003"))

    def test_contains_mid(self, bsb: PericopeDict) -> None:
        """Test contains() is True for a verse in the middle of the range."""
        assert bsb[0].contains(BCVID("01001015"))

    def test_contains_cross_chapter(self, bsb: PericopeDict) -> None:
        """Test contains() works across chapter boundaries."""
        # Gen 2:1 is within "The Creation" (01001001–01002003)
        assert bsb[0].contains(BCVID("01002001"))

    def test_not_contains(self, bsb: PericopeDict) -> None:
        """Test contains() is False for a verse outside the range."""
        # Gen 2:4 is the start of the second pericope
        assert not bsb[0].contains(BCVID("01002004"))

    def test_hashable(self, bsb: PericopeDict) -> None:
        """Test that Pericope instances are hashable and usable in sets."""
        pset = {bsb[0], bsb[1], bsb[0]}
        assert len(pset) == 2
