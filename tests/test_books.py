"""Pytest tests for biblelib.books."""
# import pytest


from biblelib import books


class TestMark(object):
    """Test basic functionality for books."""

    allbooks = books.Books()

    def test_attrs(self):
        """Test attribute values."""
        mark = self.allbooks[61]
        assert mark.usfmnumber == "41"
        assert mark.usfmname == "MRK"
        assert mark.osisID == "Mark"
        assert mark.render() == "Mark"
        assert mark.render("usfmname") == "MRK"

    def test_usfmalt(self):
        """Test the legacy USFM numbers for NT books."""
        # for OT and post-NT, alt is the same as standard
        # MAL
        assert self.allbooks[39].usfmnumberalt == self.allbooks[39].usfmnumber
        # ENO
        assert self.allbooks[87].usfmnumberalt == self.allbooks[87].usfmnumber
        # in the alternate scheme, MAT = 41 (not 40)
        assert self.allbooks[60].usfmnumberalt == "41"

    def test_comparison(self) -> None:
        """Test comparison functions."""
        assert self.allbooks[61] == self.allbooks[61]
        assert self.allbooks[61] < self.allbooks[62]
        assert self.allbooks[61] <= self.allbooks[61]
        assert self.allbooks[61] > self.allbooks[60]
        assert self.allbooks[61] >= self.allbooks[61]
        assert not (self.allbooks[61] < self.allbooks[60])
        assert not (self.allbooks[61] > self.allbooks[62])
        assert not (self.allbooks[61] != self.allbooks[61])

    def test_lookup(self):
        """Test lookup by attributes."""
        osismark = self.allbooks.fromosis("Mark")
        assert osismark.usfmname == "MRK"
        usfmnamemark = self.allbooks.fromusfmname("MRK")
        assert usfmnamemark.name == "Mark"
        logosIDmark = self.allbooks.fromlogos("bible.62")
        assert logosIDmark.name == "Mark"
        logosIDmark = self.allbooks.fromlogos(62)
        assert logosIDmark.name == "Mark"
