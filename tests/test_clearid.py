"""Test biblelib.words.clearid."""

import pytest

from biblelib.words import ClearID


class TestClearID:
    """Test basic functionality of ClearID dataclass."""

    NA1904_ID = "43001001005"
    testid = ClearID(NA1904_ID)

    def test_init(self) -> None:
        """Test initialization and attributes."""
        assert self.testid.book_ID == "43"
        assert self.testid.chapter_ID == "001"
        assert self.testid.verse_ID == "001"
        assert self.testid.word_ID == "005"
        assert self.testid.part_ID == ""
        assert repr(self.testid) == "<ClearID: 43001001005>"

    def test_fromlogos(self) -> None:
        """Test conversion from Logos-style reference."""
        assert ClearID.fromlogos("bible.62.4.8").ID == "41004008000"
        # 'title' as verse -> '000', additional bible specification
        assert ClearID.fromlogos("bible+leb2.19.3.title").ID == "19003000000"
        # USFM book ID that's not an integer like EpLao
        assert ClearID.fromlogos("bible.60.1.1").ID == "C3001001000"

    def test_invalid_length(self) -> None:
        """Test that length checks fail correction"""
        with pytest.raises(AssertionError):
            # only 10 chars
            _ = ClearID("4300100100")
        with pytest.raises(AssertionError):
            # 13 chars
            _ = ClearID("4300100100500")

    # should also test a real part_ID value
