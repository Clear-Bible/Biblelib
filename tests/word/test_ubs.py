"""Test biblelib.word.ubs.

Values are pinned to the vendored macula-hebrew/-greek mapping commits
(see biblelib.data); refresh them alongside the pinned data.
"""

import pytest

from biblelib.word import BCVID, BCVWPID
from biblelib.word.ubs import fromubs


class TestFromUBS:
    """Test basic functionality of fromubs()."""

    def test_from_ubs(self) -> None:
        """Test returned values"""
        assert fromubs("02306000600008") == [BCVWPID("230600060041")]
        assert fromubs("02306000600008{N:001}") == [BCVWPID("230600060041")]
        assert fromubs("02306000600008({N:001})") == [BCVWPID("230600060041")]
        assert fromubs("04100400300008") == [BCVWPID("410040030041")]
        assert fromubs("04100400300008") == [BCVWPID("410040030041")]
        # verse-level reference returns BCVID
        assert fromubs("00100301500000") == [BCVID("01003015")]
        assert fromubs("04100400900000") == [BCVID("41004009")]
        with pytest.raises(AssertionError):
            # missing leading zero
            assert fromubs("4100401800000") == [BCVID("41004009")]

    @pytest.mark.filterwarnings("ignore:Invalid book ID for MARBLE ID")
    def test_from_ubs_warnings(self) -> None:
        """Test returned values from from_ubs()."""
        # DC reference returns empty list
        assert fromubs("07300102100020") == []
