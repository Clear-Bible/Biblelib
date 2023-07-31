"""Pytest tests for biblelib.book."""
# import pytest


from biblelib import book


class TestMark(object):
    """Test basic functionality for books."""

    allbooks = book.Books()
    prot = book.ProtestantCanon()

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
        usfmnumbermark = self.allbooks.fromusfmnumber("41")
        assert usfmnumbermark.name == "Mark"
        usfmnumberrev = self.allbooks.fromusfmnumber("66")
        assert usfmnumberrev.name == "Revelation"
        # access via the old numbering system where MAT=41, not
        # 40. Note this doesn't change the 'correct' number on the
        # Book instance, it just uses legacy numbers for retrieval.
        usfmnumbermatt = self.allbooks.fromusfmnumber("41", legacynumbering=True)
        assert usfmnumbermatt.name == "Matthew"
        usfmnumberrev = self.allbooks.fromusfmnumber("67", legacynumbering=True)
        assert usfmnumberrev.name == "Revelation"

    def test_fromname(self):
        """Test fromname()."""
        assert self.allbooks.nameregexp.match("Genesis")
        assert self.allbooks.nameregexp.match("Song of Songs")
        # some hacked quickfixes for close-but-not-quite common names
        assert self.allbooks.fromname("Psalm")
        assert self.allbooks.fromname("Song of Solomon")
        name2cor = self.allbooks.fromname("2 Corinthians")
        assert name2cor.usfmname == "2CO"
        assert self.allbooks.nameregexp.match("1 Corinthians 13")
        assert self.allbooks.nameregexp.match("1 Corinthians 13:1")
