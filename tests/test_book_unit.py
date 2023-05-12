"""Pytest tests for biblelib.unit.book.

Not to be confused with book.book.
"""
# import pytest

from biblelib.word import BID
from biblelib.unit import book


class TestAllBookChapters:
    """Text AllBookChapters()."""

    abc = book.AllBookChapters()

    def test_init(self) -> None:
        """Test for instance."""
        assert len(self.abc) == 88
        assert len(self.abc.chapters) == 1459
        assert len(self.abc["41"]) == 16
        assert list(self.abc.keys())[-1] == "66"


class TestBook(object):
    """Test basic functionality for books."""

    testid = "41"
    mark = book.Book(identifier=BID(testid))

    def test_book(self) -> None:
        """Test for book."""
        assert self.mark.identifier.ID == self.testid
        # assert len(self.mark) == 16
        assert self.mark.versification.name == "ENG"
        assert self.mark.identifier.book_ID == "41"
        assert self.mark.parent == {}
        assert len(self.mark) == 16

    def test_enumerate(self) -> None:
        """Test for enumerate."""
        # check a stop enumeration
        range4 = self.mark.enumerate(4)
        assert range4[0].identifier.ID == "41001"
        assert range4[-1].identifier.ID == "41004"
        # check a start, stop enumeration
        range2_4 = self.mark.enumerate(2, 4)
        assert range2_4[0].identifier.ID == "41002"
        assert range2_4[-1].identifier.ID == "41004"
        # check the last verse of the book
        markrange = self.mark.enumerate(self.mark.lastchapter)
        assert markrange[0].identifier.ID == "41001"
        assert markrange[-1].identifier.ID == "41016"
