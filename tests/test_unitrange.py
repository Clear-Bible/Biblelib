"""Pytest tests for biblelib.unit.range."""
import pytest

from biblelib.word import BCID, BCVID
from biblelib.unit import unitrange


class TestChapterRange(object):
    """Test basic functionality for ChapterRange."""

    testrange = unitrange.ChapterRange(start=BCID("41001"), end=BCID("41016"))

    def test_init(self) -> None:
        """Test initialization."""
        # must be in same book
        with pytest.raises(Exception):
            unitrange.ChapterRange(start=BCID("40001"), end=BCID("41001"))
        # start must < end
        with pytest.raises(Exception):
            unitrange.ChapterRange(start=BCID("41002"), end=BCID("41001"))

    def test_enumerate_vacuous(self) -> None:
        """Test for vacuous enumeration."""
        # vacuous range
        vacrange = unitrange.ChapterRange(start=BCID("41001"), end=BCID("41001"))
        enumerated = vacrange.enumerate()
        assert len(enumerated) == 1
        assert enumerated[0] == vacrange.end

    def test_enumerate(self) -> None:
        """Test for enumerate."""
        # vacuous range
        enumerated = self.testrange.enumerate()
        assert len(enumerated) == 16


class TestVerseRange(object):
    """Test basic functionality for VerseRange."""

    testrange_samechap = unitrange.VerseRange(start=BCVID("41001002"), end=BCVID("41001005"))
    testrange_onechap = unitrange.VerseRange(start=BCVID("41001040"), end=BCVID("41002002"))
    testrange_twochap = unitrange.VerseRange(start=BCVID("41001040"), end=BCVID("41003002"))

    def test_init(self) -> None:
        """Test initialization."""
        # must be in same book
        with pytest.raises(Exception):
            unitrange.VerseRange(start=BCVID("40001001"), end=BCVID("41001001"))
        # start must < end
        with pytest.raises(Exception):
            unitrange.ChapterRange(start=BCVID("41002001"), end=BCVID("41001001"))

    def test_enumerate_vacuous(self) -> None:
        """Test for vacuous enumeration."""
        # vacuous range
        vacrange = unitrange.VerseRange(start=BCVID("41001004"), end=BCVID("41001004"))
        enumerated = vacrange.enumerate()
        assert len(enumerated) == 1
        assert enumerated[0] == vacrange.end

    def test_enumerate_samechap(self) -> None:
        """Test for enumerating samechap."""
        # vacuous range
        assert len(self.testrange_samechap.enumerate()) == 4

    def test_enumerate_onechap(self) -> None:
        """Test for enumerating onechap."""
        # vacuous range
        assert len(self.testrange_onechap.enumerate()) == 8

    def test_enumerate_twochap(self) -> None:
        """Test for enumerating twochap."""
        # vacuous range
        assert len(self.testrange_twochap.enumerate()) == 36
