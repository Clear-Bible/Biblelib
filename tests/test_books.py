"""Pytest tests for biblelib.books."""
# import pytest


from biblelib import books


class TestMark(object):
    """Test basic functionality for books."""

    allbooks = books.Books()
    prot = books.ProtestantCanon()

    def test_attrs_gen(self):
        """Test attribute values for Genesis."""
        # will need updating if the list changes
        gen = self.allbooks["GEN"]
        assert str(gen) == "<Book: GEN>"
        assert gen.usfmnumber == "01"
        assert gen.osisID == "Gen"
        assert gen.altname == ""
        assert gen.render() == "Gen"
        assert gen.render("usfmname") == "GEN"
        assert gen.render("logosID") == "bible.1"

    def test_attrs_mark(self):
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
        assert self.prot["MRK"] == self.prot["MRK"]
        assert self.prot["MRK"] < self.prot["LUK"]
        assert self.prot["MRK"] <= self.prot["MRK"]
        assert self.prot["MRK"] > self.prot["MAT"]
        assert self.prot["MRK"] >= self.prot["MRK"]
        assert not (self.prot["MRK"] < self.prot["MAT"])
        assert not (self.prot["MRK"] > self.prot["LUK"])
        assert not (self.prot["MRK"] != self.prot["MRK"])

    def test_sorted(self):
        """Test sorting in canon order."""
        randbooks = [self.prot["1CO"], self.prot["ECC"], self.prot["LUK"], self.prot["MRK"]]
        assert [b.usfmname for b in sorted(randbooks)] == ["ECC", "MRK", "LUK", "1CO"]

    def test_lookup(self):
        """Test lookup by attributes."""
        osismark = self.allbooks.fromosis("Mark")
        assert osismark.usfmname == "MRK"
        logosIDmark = self.allbooks.fromlogos("bible.62")
        assert logosIDmark.name == "Mark"
        logosIDmark = self.allbooks.fromlogos(62)
        assert logosIDmark.name == "Mark"
