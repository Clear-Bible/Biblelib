"""Test biblelib.word.ubs. Requires a network connection."""

import pytest

from biblelib.word import BCVID, BCVWPID
from biblelib.word.ubs import fromubs


class TestFromUBS:
    """Test basic functionality of fromubs()."""

    def test_from_ubs(self) -> None:
        """Test returned values"""
        assert fromubs("02306000600008") == [BCVWPID("23060006004")]
        assert fromubs("02306000600008{N:001}") == [BCVWPID("23060006004")]
        assert fromubs("02306000600008({N:001})") == [BCVWPID("23060006004")]
        assert fromubs("04100400300008") == [BCVWPID("41004003004")]
        assert fromubs("04100400300008") == [BCVWPID("41004003004")]
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
