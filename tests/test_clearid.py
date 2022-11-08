"""Test biblelib.words.clearid."""

from biblelib.words.clearid import ClearID


class TestClearID:
    """Test basic functionality of ClearID dataclass."""

    NA1904_ID = "43001001005"
    testid = ClearID(NA1904_ID)

    def test_init(self) -> None:
        """Test initialization and attributes."""
        self.testid.book_ID == "43"
        self.testid.chapter_ID == "001"
        self.testid.verse_ID == "001"
        self.testid.word_ID == "005"
        self.testid.part_ID == ""
        repr(self.testid) == "<ClearID: 43001001005>"

    # should also test a real part_ID value
