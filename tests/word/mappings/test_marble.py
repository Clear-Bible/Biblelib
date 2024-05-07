"""Test biblelib.word.mappings.marble"""

import pytest

from biblelib.word.mappings import Mapper


class TestMapper:
    """Test basic functionality of Mapper."""

    m = Mapper()

    def test_init(self) -> None:
        """Test initialization and attributes."""
        assert self.m.to_macula("00100100100016") == ["o010010010061"]
        assert self.m.to_macula("04100604500034") == ["n41006045017"]
        # strip suffix
        assert self.m.to_macula("02306000600008{N:001}") == ["o230600060041"]
        # no mapping for this valid GNT reference
        assert self.m.to_macula("04000401600012") == []

    @pytest.mark.filterwarnings("ignore:Invalid book ID for MARBLE ID")
    def test_dc_reference(self) -> None:
        """Test DC reference, without warnings."""
        # no mapping for this DC reference
        assert self.m.to_macula("07700101700022") == []
