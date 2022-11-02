"""Pytest tests for biblelib.books."""
# import pytest


from biblelib import books


class TestMark(object):
    """Test basic functionality for books."""

    # assumes test is run from Biblelib directory
    sourcefile = "biblelib/books/books.tsv"
    allbooks = books.Books(sourcefile=sourcefile)

    def test_attrs(self):
        """Test attribute values."""
        # will need updating if the list changes
        assert len(self.allbooks) == 101
        mark = self.allbooks["MRK"]
        assert str(mark) == "<Book: MRK>"
        assert mark.usfmnumber == "41"
        assert mark.osisID == "Mark"
        assert mark.altname == "The Gospel according to Mark"
        assert mark.render() == "Mark"
        assert mark.render("usfmname") == "MRK"
        assert mark.render("logosID") == "bible.62"

    def test_usfmalt(self):
        """Test the legacy USFM numbers for NT books."""
        # for OT and post-NT, alt is the same as standard
        # MAL
        assert self.allbooks["MAL"].usfmnumberalt == self.allbooks["MAL"].usfmnumber
        # ENO
        assert self.allbooks["ENO"].usfmnumberalt == self.allbooks["ENO"].usfmnumber
        # in the alternate scheme, MAT = 41 (not 40)
        assert self.allbooks["MAT"].usfmnumberalt == "41"

    def test_comparison(self) -> None:
        """Test comparison functions."""
        assert self.allbooks["MRK"] == self.allbooks["MRK"]
        assert self.allbooks["MRK"] < self.allbooks["LUK"]
        assert self.allbooks["MRK"] <= self.allbooks["MRK"]
        assert self.allbooks["MRK"] > self.allbooks["MAT"]
        assert self.allbooks["MRK"] >= self.allbooks["MRK"]
        assert not (self.allbooks["MRK"] < self.allbooks["MAT"])
        assert not (self.allbooks["MRK"] > self.allbooks["LUK"])
        assert not (self.allbooks["MRK"] != self.allbooks["MRK"])

    def test_lookup(self):
        """Test lookup by attributes."""
        osismark = self.allbooks.fromosis("Mark")
        assert osismark.usfmname == "MRK"
        logosIDmark = self.allbooks.fromlogos("bible.62")
        assert logosIDmark.name == "Mark"
        logosIDmark = self.allbooks.fromlogos(62)
        assert logosIDmark.name == "Mark"
