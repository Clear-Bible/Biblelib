"""Test biblelib.word.mappings."""

import pytest

from biblelib.word.mappings import WLCMMapping, WLCMMappings


# Example mapping: JHN 1:1
TESTMAPPING = WLCMMapping(
    MACULA_IDs="o010010010061",
    MARBLE_IDs="00100100100016",
)


class TestWLCMMapping:
    """Test basic functionality of WLCMMapping dataclass."""

    def test_init(self) -> None:
        """Test initialization and attributes."""
        assert TESTMAPPING.MACULA_IDs == "o010010010061"
        # this form should have correct NFC normalization
        assert TESTMAPPING.MARBLE_IDs == "00100100100016"
        # needs the leading canon prefix
        with pytest.raises(AssertionError):
            _ = WLCMMapping(
                MACULA_IDs="010010010061",
                MARBLE_IDs="00100100100016",
            )


class TestWLCMMappings:
    """Test basic functionality of WLCMMappings class."""

    wlcm = WLCMMappings()

    def test_init(self) -> None:
        """Test initialization: reading, and resulting list length."""
        # FRAGILE!
        assert len(self.wlcm) == 420059

    def test_marble2macula(self) -> None:
        """Test marble2macula method."""
        assert self.wlcm.marble2macula("00100100100016") == ["o010010010061"]
        # check two-token mapping
        assert self.wlcm.marble2macula("00100101100032") == ["o010010110132", "o010010110133"]
        # must be in correct book range
        with pytest.raises(AssertionError):
            self.wlcm.marble2macula("00000401600012")
        with pytest.raises(AssertionError):
            self.wlcm.marble2macula("04000401600012")
