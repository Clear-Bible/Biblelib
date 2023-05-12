"""Pytest tests for biblelib.unit.chapter."""
# import pytest

from biblelib.word import BCID
from biblelib.unit import chapter


class TestChapter(object):
    """Test basic functionality for chapters."""

    testid = "41004"
    mark_4 = chapter.Chapter(identifier=BCID(testid))

    def test_chapter(self) -> None:
        """Test for chapter."""
        assert self.mark_4.identifier.ID == self.testid
        assert len(self.mark_4) == 41
        assert self.mark_4.versification.name == "ENG"
        assert self.mark_4.book_ID == "41"
        assert self.mark_4.parent["Book"].name == "Mark"
        assert self.mark_4.lastverse == 41

    def test_ChapterVerses(self) -> None:
        """Test for ChapterVerses."""
        assert self.mark_4.chapverses.chapter_ID == "41004"
        assert self.mark_4.chapverses.end_ID == "41004041"
        chapters = chapter.Chapters()
        assert len(chapters) == 1459
        assert list(chapters.keys())[0] == "01001"
        gen1cv = list(chapters.values())[0]
        assert gen1cv.end_ID == "01001031"

    def test_chapters(self) -> None:
        """Test for _chapters."""
        assert len(chapter.Chapter._chapters) == 1459

    def test_enumerate(self) -> None:
        """Test for enumerate."""
        # check a stop enumeration
        range4 = self.mark_4.enumerate(4)
        assert range4[0].identifier.ID == "41004001"
        assert range4[-1].identifier.ID == "41004004"
        # check a start, stop enumeration
        range2_4 = self.mark_4.enumerate(2, 4)
        assert range2_4[0].identifier.ID == "41004002"
        assert range2_4[-1].identifier.ID == "41004004"
        # check the last verse of the chapter
        markrange = self.mark_4.enumerate(self.mark_4.lastverse)
        assert markrange[0].identifier.ID == "41004001"
        assert markrange[-1].identifier.ID == "41004041"
