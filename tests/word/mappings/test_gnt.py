"""Test biblelib.word.mappings."""

from biblelib.word.mappings import GNTMapping, GNTMappings


# Example mapping: JHN 1:1
TESTMAPPING = GNTMapping(
    NA1904_ID="n43001001005",
    NA1904_Text="Λόγος,",
    NA27_ID="43001001005",
    NA28_ID="43001001005",
    SBLGNT_ID="n43001001005",
    SBLGNT_Text="λόγος,",
    MARBLE_ID="04300100100010",
)


class TestGNTMapping:
    """Test basic functionality of GNTMapping dataclass."""

    def test_init(self) -> None:
        """Test initialization and attributes."""
        assert TESTMAPPING.NA1904_ID == "n43001001005"
        # this form should have correct NFC normalization
        assert TESTMAPPING.NA1904_Text == "Λόγος,"


class TestGNTMappings:
    """Test basic functionality of GNTMappings class."""

    gnt = GNTMappings()

    def test_init(self) -> None:
        """Test initialization: reading, and resulting list length."""
        # FRAGILE!
        assert len(self.gnt) == 138750

    def test_marble2sblgnt(self) -> None:
        """Test marble2sblgnt method."""
        assert self.gnt.marble2sblgnt("04100604500034") == "n41006045017"
        # no mapping for this
        assert self.gnt.marble2sblgnt("04000401600012") == ""

    def test_na282sblgnt(self) -> None:
        """Test na282sblgnt method."""
        assert self.gnt.na282sblgnt("41004003001") == "n41004003001"
        # no mapping for this
        assert self.gnt.na282sblgnt("40004016006") == ""
