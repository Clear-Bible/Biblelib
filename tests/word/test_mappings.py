"""Test biblelib.word.mappings."""

from biblelib.word import Mapping, Mappings


# Example mapping: JHN 1:1
TESTMAPPING = Mapping(
    NA1904_ID="43001001005",
    NA1904_Text="Λόγος,",
    NA27_ID="43001001005",
    NA28_ID="43001001005",
    SBLGNT_ID="43001001005",
    SBLGNT_Text="λόγος,",
    MARBLE_ID="04300100100010",
)


class TestMapping:
    """Test basic functionality of Mapping dataclass."""

    def test_init(self) -> None:
        """Test initialization and attributes."""
        assert TESTMAPPING.NA1904_ID == "43001001005"
        # this form should have correct NFC normalization
        assert TESTMAPPING.NA1904_Text == "Λόγος,"


class TestMappings:
    """Test basic functionality of Mappings class."""

    def test_init(self) -> None:
        """Test initialization: reading, and resulting list length."""
        # Assumes a local copy of the macula-greek repo
        m = Mappings()
        # FRAGILE!
        assert len(m) == 138751
