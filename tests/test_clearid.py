"""Test biblelib.words.clearid."""

from biblelib.words.clearid import ClearID


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
        """"""

    # should also test a real part_ID value
