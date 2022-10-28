"""Pytest tests for biblelib.books."""
# import pytest


from biblelib import books


class TestMark(object):
    """Test basic functionality for books."""

    allbooks = books.Books()

    def test_attrs(self):
        """Test attribute values."""
        mark = self.allbooks[40]
        assert mark.usfmnumber == "42"
        assert mark.usfmname == "MRK"
        assert mark.osisID == "Mark"
        assert mark.render("usfmname") == "MRK"

    def test_comparison(self) -> None:
        """Test comparison functions."""
        assert self.allbooks[40] == self.allbooks[40]
        assert self.allbooks[40] < self.allbooks[41]
        assert self.allbooks[40] <= self.allbooks[40]
        assert self.allbooks[40] > self.allbooks[39]
        assert self.allbooks[40] >= self.allbooks[40]
        assert not (self.allbooks[40] < self.allbooks[39])
        assert not (self.allbooks[40] > self.allbooks[41])
        assert not (self.allbooks[40] != self.allbooks[40])

    def test_lookup(self):
        """Test lookup by attributes."""
        osismark = self.allbooks.fromosis("Mark")
        assert osismark.usfmname == "MRK"
        usfmnamemark = self.allbooks.fromusfmname("MRK")
        assert usfmnamemark.name == "Mark"
