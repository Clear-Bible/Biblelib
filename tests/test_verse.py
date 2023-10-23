"""Pytest tests for biblelib.unit.verse."""
# import pytest

from biblelib.word import BCVID
from biblelib.unit import verse


class TestVerse(object):
    """Test basic functionality for verses."""

    def test_verse(self) -> None:
        """Test for verse."""
        testid = "41004003"
        mark_4_3 = verse.Verse(inst=BCVID(testid))
        assert mark_4_3.identifier.ID == testid
        assert len(mark_4_3) == 0
        assert mark_4_3.versification.name == "ENG"
