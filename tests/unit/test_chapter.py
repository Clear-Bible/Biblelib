"""Pytest tests for biblelib.unit.chapter."""

# import pytest

from biblelib.word import BCID
from biblelib.unit import chapter


class TestChapterVerses:
    """Test basic functionality for ChapterVerses."""

    mark_4: chapter.ChapterVerses = chapter.ChapterVerses(chapter_ID="41004",
                                                          end_ID="41004041")

    def test_init(self) -> None:
        """Test for __init__."""
        assert self.mark_4.chapter_ID == "41004"
        assert self.mark_4.end_ID == "41004041"
        assert self.mark_4.book_ID == "41"
        assert self.mark_4.lastverse == 41
        assert repr(self.mark_4) == 'ChapterVerses(chapter_ID="41004", end_ID="41004041")'


class TestChapters:
    """Test basic functionality for Chapters."""
    chpts: chapter.Chapters = chapter.Chapters()

    def test_init(self) -> None:
        """Test for __init__."""
        assert len(self.chpts) == 1459
        assert self.chpts["01001"].chapter_ID == "01001"
        assert self.chpts["01001"].end_ID == "01001031"


class TestChapter(object):
    """Test basic functionality for chapters."""

    testid: str = "41004"
    mark_4: chapter.Chapter = chapter.Chapter(inst=BCID(testid))

    def test_chapter(self) -> None:
        """Test for chapter."""
        assert self.mark_4.inst.ID == self.testid
        assert len(self.mark_4) == 41
        assert self.mark_4.versification.name == "ENG"
        assert self.mark_4.book_ID == "41"
        assert self.mark_4.parentbook.name == "Mark"
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
        assert range4[0].inst.ID == "41004001"
        assert range4[-1].inst.ID == "41004004"
        # check a start, stop enumeration
        range2_4 = self.mark_4.enumerate(2, 4)
        assert range2_4[0].inst.ID == "41004002"
        assert range2_4[-1].inst.ID == "41004004"
        # check the last verse of the chapter
        markrange = self.mark_4.enumerate(self.mark_4.lastverse)
        assert markrange[0].inst.ID == "41004001"
        assert markrange[-1].inst.ID == "41004041"
