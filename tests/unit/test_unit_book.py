"""Pytest tests for biblelib.unit.book.

Not to be confused with book.book.
"""

# import pytest

from biblelib.word import BID
from biblelib.unit.book import BookChapters, Book, AllBookChapters


class TestBookChapters:
    """Test BookChapters().

    This is initialized by AllBookChapters(), but testing never hurts.
    """

    mrk = BookChapters("41", "41016", start_ID="41001")

    def test_init(self) -> None:
        """Test for instance."""
        assert self.mrk.book_ID == "41"
        assert self.mrk.end_ID == "41016"
        assert self.mrk.start_ID == "41001"

    def test_from_book_tuple(self) -> None:
        """Test for from_book_tuple."""
        assert BookChapters.from_book_tuple((82, {1: 21, 2: 22, 3: 18})) == \
            BookChapters(book_ID='61', end_ID='61003', start_ID='61001', name='2PE')


class TestAllBookChapters:
    """Text AllBookChapters()."""

    abc = AllBookChapters()

    def test_init(self) -> None:
        """Test for instance."""
        assert len(self.abc) == 88
        assert len(self.abc.chapters) == 1459
        assert len(self.abc["41"]) == 16
        assert list(self.abc.keys())[-1] == "66"


class TestBook(object):
    """Test basic functionality for books."""

    testid = "41"
    mark = Book(inst=BID(testid))

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
