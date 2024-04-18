"""Pytest tests for biblelib.book."""

# import pytest


from biblelib import book


class TestMark(object):
    """Test basic functionality for books."""

    allbooks = book.Books()
    prot = book.ProtestantCanon()

    def test_attrs_gen(self) -> None:
        """Test attribute values for Genesis."""
        # will need updating if the list changes
        gen = self.allbooks["GEN"]
        assert str(gen) == "<Book: GEN>"
        assert gen.usfmnumber == "01"
        assert gen.osisID == "Gen"
        assert gen.biblia == "Ge"
        assert gen.altname == ""
        assert gen.render() == "Gen"
        assert gen.render("usfmname") == "GEN"
        assert gen.render("logosID") == "bible.1"
        assert gen.logosURI == "https://ref.ly/logosref/bible.1"
        # need to drop nrsv
        assert gen.bibliaURI == "https://biblia.com/books/nrsv/Ge"

    def test_attrs_mark(self) -> None:
        """Test attribute values."""
        # will need updating if the list changes
        assert len(self.allbooks) == 101
        mark = self.allbooks["MRK"]
        assert str(mark) == "<Book: MRK>"
        assert mark.usfmnumber == "41"
        assert self.allbooks.fromosis("Mark").name == "Mark"
        assert mark.osisID == "Mark"
        assert mark.biblia == "Mk"
        assert mark.altname == "The Gospel according to Mark"
        assert mark.render() == "Mark"
        assert mark.render("usfmname") == "MRK"
        assert mark.render("logosID") == "bible.62"
        assert mark.logosURI == "https://ref.ly/logosref/bible.62"
        # need to drop nrsv
        assert mark.bibliaURI == "https://biblia.com/books/nrsv/Mk"

    def test_usfmalt(self) -> None:
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

    def test_sorted(self) -> None:
        """Test sorting in canon order."""
        randbooks = [self.prot["1CO"], self.prot["ECC"], self.prot["LUK"], self.prot["MRK"]]
        assert [b.usfmname for b in sorted(randbooks)] == ["ECC", "MRK", "LUK", "1CO"]

    def test_lookup(self) -> None:
        """Test lookup by attributes."""
        bibliamark = self.allbooks.frombiblia("Mk")
        assert bibliamark.usfmname == "MRK"
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

    def test_fromname(self) -> None:
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
