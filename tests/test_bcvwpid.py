"""Test biblelib.words.bcvwpid."""

import pytest

from biblelib.words import BCVWPID
from biblelib.words.bcvwpid import pad3


class TestPad3:
    """Test basic functionality of pad3()."""

    def test_return(self) -> None:
        """Test returned values"""
        assert pad3("title") == "000"
        assert pad3("1") == "001"
        assert pad3("23") == "023"
        with pytest.raises(ValueError):
            # not convertible to an int
            _ = pad3("a")
        with pytest.raises(AssertionError):
            # too long
            _ = pad3("1234")


class TestBCVWPID:
    """Test basic functionality of BCVWPID dataclass."""

    NA1904_ID = "43001001005"
    testid = BCVWPID(NA1904_ID)

    def test_init(self) -> None:
        """Test initialization and attributes."""
        assert self.testid.book_ID == "43"
        assert self.testid.chapter_ID == "001"
        assert self.testid.verse_ID == "001"
        assert self.testid.word_ID == "005"
        assert self.testid.part_ID == ""
        assert repr(self.testid) == "<BCVWPID: 43001001005>"

    def test_init_with_part(self) -> None:
        """Test initialization and attributes for an ID with a part."""
        testid = BCVWPID("010020030011")
        assert testid.book_ID == "01"
        assert testid.chapter_ID == "002"
        assert testid.verse_ID == "003"
        assert testid.word_ID == "001"
        assert testid.part_ID == "1"
        assert repr(testid) == "<BCVWPID: 010020030011>"

    def test_fromusfm(self) -> None:
        """Test conversion from USFM-style reference."""
        # early OT books should be zero-padded
        assert BCVWPID.fromusfm("Gen 3:16").ID == "01003016000"
        with pytest.raises(AssertionError):
            _ = BCVWPID.fromusfm("Genesis 3:16")
        assert BCVWPID.fromusfm("MRK 4:8").ID == "41004008000"
        with pytest.raises(AssertionError):
            _ = BCVWPID.fromusfm("Mark 3:16")

    def test_fromlogos(self) -> None:
        """Test conversion from Logos-style reference."""
        # early OT books should be zero-padded
        assert BCVWPID.fromlogos("bible.1.2.3").ID == "01002003000"
        assert BCVWPID.fromlogos("bible.62.4.8").ID == "41004008000"
        # 'title' as verse -> '000', additional bible specification
        assert BCVWPID.fromlogos("bible+leb2.19.3.title").ID == "19003000000"
        # USFM book ID that's not an integer like EpLao
        assert BCVWPID.fromlogos("bible.60.1.1").ID == "C3001001000"

    def test_invalid_length(self) -> None:
        """Test that length checks fail correction"""
        with pytest.raises(AssertionError):
            # only 10 chars
            _ = BCVWPID("4300100100")
        with pytest.raises(AssertionError):
            # 13 chars
            _ = BCVWPID("4300100100500")

    # should also test a real part_ID value
