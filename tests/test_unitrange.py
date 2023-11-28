"""Pytest tests for biblelib.unit.range."""

import pytest

from biblelib.word import BCID, BCVID
from biblelib.unit import Chapter, Verse, unitrange


class TestChapterRange(object):
    """Test basic functionality for ChapterRange."""

    testrange = unitrange.ChapterRange(startid=BCID("41001"), endid=BCID("41016"))

    def test_init(self) -> None:
        """Test initialization."""
        # must be in same book
        with pytest.raises(Exception):
            unitrange.ChapterRange(startid=BCID("40001"), endid=BCID("41001"))
        # startid must < endid
        with pytest.raises(Exception):
            unitrange.ChapterRange(startid=BCID("41002"), endid=BCID("41001"))

    def test_enumerate_vacuous(self) -> None:
        """Test for vacuous enumeration."""
        # vacuous range
        vacrange = unitrange.ChapterRange(startid=BCID("41001"), endid=BCID("41001"))
        enumerated = vacrange.enumerate()
        assert isinstance(enumerated[0], Chapter)
        assert len(enumerated) == 1
        assert enumerated[0] == Chapter(vacrange.endid)

    def test_enumerate(self) -> None:
        """Test for enumerate."""
        # vacuous range
        enumerated = self.testrange.enumerate()
        assert len(enumerated) == 16


class TestVerseRange(object):
    """Test basic functionality for VerseRange."""

    testrange_samechap = unitrange.VerseRange(startid=BCVID("41001002"), endid=BCVID("41001005"))
    testrange_onechap = unitrange.VerseRange(startid=BCVID("41001040"), endid=BCVID("41002002"))
    testrange_twochap = unitrange.VerseRange(startid=BCVID("41001040"), endid=BCVID("41003002"))

    def test_init(self) -> None:
        """Test initialization."""
        # must be in same book
        with pytest.raises(Exception):
            unitrange.VerseRange(startid=BCVID("40001001"), endid=BCVID("41001001"))
        # startid must < endid
        with pytest.raises(Exception):
            unitrange.ChapterRange(startid=BCVID("41002001"), endid=BCVID("41001001"))

    def test_enumerate_vacuous(self) -> None:
        """Test for vacuous enumeration."""
        # vacuous range
        vacrange = unitrange.VerseRange(startid=BCVID("41001004"), endid=BCVID("41001004"))
        enumerated = vacrange.enumerate()
        assert len(enumerated) == 1
        # ensure enumeration returns instances of the correct type
        assert enumerated[0] == Verse(BCVID("41001004"))
        assert enumerated[0] == Verse(vacrange.endid)

    def test_enumerate_samechap(self) -> None:
        """Test for enumerating samechap."""
        enumerated = self.testrange_samechap.enumerate()
        assert isinstance(enumerated[0], Verse)
        # vacuous range
        assert len(enumerated) == 4

    def test_enumerate_onechap(self) -> None:
        """Test for enumerating onechap."""
        enumerated = self.testrange_onechap.enumerate()
        assert isinstance(enumerated[0], Verse)
        # vacuous range
        assert len(enumerated) == 8

    def test_enumerate_twochap(self) -> None:
        """Test for enumerating twochap."""
        enumerated = self.testrange_twochap.enumerate()
        assert isinstance(enumerated[0], Verse)
        # vacuous range
        assert len(enumerated) == 36
