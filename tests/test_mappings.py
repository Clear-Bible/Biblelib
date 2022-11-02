"""Test biblelib.words.mappings."""

import pytest
from biblelib.words import mappings


# Example mapping: JHN 1:1
TESTMAPPING = mappings.Mapping(
    NA1904_ID="43001001005",
    NA1904_Text="Λόγος,",
    NA27_ID="43001001005",
    NA28_ID="43001001005",
    SBLGNT_ID="43001001005",
    SBLGNT_Text="λόγος,",
    MARBLE_ID="04300100100010",
)


class TestClearID:
    """Test basic functionality of ClearID dataclass."""

    testid = mappings.ClearID(TESTMAPPING.NA1904_ID)

    def test_init(self) -> None:
        """Test initialization and attributes."""
        self.testid.book_ID == "43"
        self.testid.chapter_ID == "001"
        self.testid.verse_ID == "001"
        self.testid.word_ID == "005"
        self.testid.part_ID == ""
        repr(self.testid) == "<ClearID: 43001001005>"


class TestMapping:
    """Test basic functionality of Mapping dataclass."""

    def test_init(self) -> None:
        """Test initialization and attributes."""
        TESTMAPPING.NA1904_ID = "43001001005"
        TESTMAPPING.NA1904_Text = "Λόγος,"


class TestMappings:
    """Test basic functionality of Mappings class."""

    def test_init(self) -> None:
        """Test initialization: reading, and resulting list length."""
        # this path assumes tests are run from the Biblelib directory, and
        # there's a local copy of the macula-greek repo
        m = mappings.Mappings("../macula-greek/sources/Clear/mappings/mappings-GNT-stripped.tsv")
        # fragile?
        len(m) == 138804
