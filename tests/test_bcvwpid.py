"""Test biblelib.word.bcvwpid."""

import pytest

from biblelib.word import fromlogos, fromname, fromosis, fromusfm, BID, BCID, BCVID, BCVWPID, simplify

from biblelib.word.bcvwpid import pad3


class TestPad3:
    """Test basic functionality of pad3()."""

    def test_return(self) -> None:
        """Test returned values"""
        assert pad3("title") == "000"
        assert pad3("1") == "001"
        assert pad3("23") == "023"
        with pytest.raises(ValueError):
            # not convertible to an int
            _ = pad3("a")
        with pytest.raises(AssertionError):
            # too long
            _ = pad3("1234")


class TestFromLogos:
    """Test basic functionality of fromlogos()."""

    def test_fromlogos_book(self) -> None:
        """Test returned values"""
        assert fromlogos("bible.1") == BID("01")
        assert fromlogos("bible.62") == BID("41")
        assert fromlogos("62") == BID("41")
        # this fails in
        with pytest.raises(AssertionError):
            # out of range
            _ = fromlogos("00")
        with pytest.raises(AssertionError):
            # out of range
            _ = fromlogos("89")

    def test_fromlogos_chapter(self) -> None:
        """Test returned values"""
        assert fromlogos("bible.1.2") == BCID("01002")
        assert fromlogos("bible.1.12") == BCID("01012")
        assert fromlogos("bible.19.119") == BCID("19119")
        assert fromlogos("62.4") == BCID("41004")

    def test_fromlogos_chapter_verse(self) -> None:
        """Test returned values"""
        assert fromlogos("bible.1.2.3") == BCVID("01002003")
        assert fromlogos("bible.1.12.10") == BCVID("01012010")
        assert fromlogos("bible.19.119.1") == BCVID("19119001")
        assert fromlogos("62.4.1") == BCVID("41004001")


class TestFromName:
    """Test basic functionality of fromname()."""

    def test_fromname_book(self) -> None:
        """Test returned values"""
        assert fromname("Genesis") == BID("01")
        assert fromname("1 Corinthians") == BID("46")
        # fixed bug
        assert fromname("Esther") == BID("17")
        assert fromname("Song of Songs") == BID("22")
        # not handling alternate names yet
        # assert fromname("Song of Solomon") == BID("22")
        # should probably test some DC books too
        with pytest.raises(AssertionError):
            # cannot handle USFM names
            _ = fromname("1CO")

    def test_fromname_case(self) -> None:
        """Test returned values"""
        with pytest.raises(AssertionError):
            # wrong case
            _ = fromname("1 corinthians")

    def test_fromname_chapter(self) -> None:
        """Test returned values"""
        assert fromname("Genesis 2") == BCID("01002")
        assert fromname("Genesis 12") == BCID("01012")
        assert fromname("Psalms 119") == BCID("19119")
        assert fromname("Mark 4") == BCID("41004")

    def test_fromname_chapter_verse(self) -> None:
        """Test returned values"""
        assert fromname("Genesis 2:3") == BCVID("01002003")
        assert fromname("Genesis 12:10") == BCVID("01012010")
        assert fromname("Psalms 119:1") == BCVID("19119001")
        assert fromname("Mark 4:1") == BCVID("41004001")
        with pytest.raises(AssertionError):
            # space not allowed here
            _ = fromname("1 Corinthians 13 3")


class TestFromOsis:
    """Test basic functionality of fromosis()."""

    def test_fromosis_book(self) -> None:
        """Test returned values"""
        assert fromosis("Gen") == BID("01")
        assert fromosis("Mark") == BID("41")

    def test_fromosis_case(self) -> None:
        """Test returned values"""
        assert fromosis("1Cor") == BID("46")
        with pytest.raises(KeyError):
            # wrong case
            _ = fromosis("1cor")
        with pytest.raises(KeyError):
            # wrong case
            _ = fromosis("1COR")

    def test_fromosis_chapter(self) -> None:
        """Test returned values"""
        assert fromosis("Gen 2") == BCID("01002")
        assert fromosis("Gen 12") == BCID("01012")
        assert fromosis("Ps 119") == BCID("19119")
        assert fromosis("Mark 4") == BCID("41004")

    def test_fromosis_chapter_verse(self) -> None:
        """Test returned values"""
        assert fromosis("Gen 2:3") == BCVID("01002003")
        assert fromosis("Gen 12:10") == BCVID("01012010")
        assert fromosis("Ps 119:1") == BCVID("19119001")
        assert fromosis("Mark 4:1") == BCVID("41004001")


class TestFromUsfm:
    """Test basic functionality of fromusfm()."""

    def test_fromusfm_book(self) -> None:
        """Test returned values"""
        assert fromusfm("GEN") == BID("01")
        assert fromusfm("MRK") == BID("41")

    def test_fromusfm_chapter(self) -> None:
        """Test returned values"""
        assert fromusfm("GEN 2") == BCID("01002")
        assert fromusfm("GEN 12") == BCID("01012")
        assert fromusfm("PSA 119") == BCID("19119")
        assert fromusfm("MRK 4") == BCID("41004")

    def test_fromusfm_chapter_verse(self) -> None:
        """Test returned values"""
        assert fromusfm("GEN 2:3") == BCVID("01002003")
        assert fromusfm("GEN 12:10") == BCVID("01012010")
        assert fromusfm("PSA 119:1") == BCVID("19119001")
        assert fromusfm("MRK 4:1") == BCVID("41004001")


class TestBID:
    """Test basic functionality of BID dataclass."""

    genid = "01"
    markid = "41"

    def test_init(self) -> None:
        """Test initialization and attributes."""
        assert BID(self.genid).book_ID == self.genid
        assert BID(self.markid).book_ID == self.markid

    # def test_fromusfm(self) -> None:
    #     """Test fromusfm()."""
    #     assert BID.fromusfm("GEN").book_ID == self.genid
    #     assert BID.fromusfm("MRK").book_ID == self.markid

    # def test_fromlogos(self) -> None:
    #     """Test fromlogos()."""
    #     assert BID.fromlogos("bible.62").book_ID == self.markid


class TestBCVID:
    """Test basic functionality of BCVID dataclass."""

    NA1904_ID = "43001001"
    testid = BCVID(NA1904_ID)

    def test_init(self) -> None:
        """Test initialization and attributes."""
        assert self.testid.book_ID == "43"
        assert self.testid.chapter_ID == "001"
        assert self.testid.verse_ID == "001"
        assert repr(self.testid) == "BCVID('43001001')"

    # def test_fromusfm(self) -> None:
    #     """Test conversion from USFM-style reference."""
    #     # early OT books should be zero-padded
    #     assert BCVID.fromusfm("Gen 3:16").ID == "01003016"
    #     with pytest.raises(AssertionError):
    #         _ = BCVID.fromusfm("Genesis 3:16")
    #     assert BCVID.fromusfm("MRK 4:8").ID == "41004008"
    #     with pytest.raises(AssertionError):
    #         _ = BCVID.fromusfm("Mark 3:16")

    # def test_fromlogos(self) -> None:
    #     """Test conversion from Logos-style reference."""
    #     # early OT books should be zero-padded
    #     assert BCVID.fromlogos("bible.1.2.3").ID == "01002003"
    #     assert BCVID.fromlogos("bible.62.4.8").ID == "41004008"
    #     # 'title' as verse -> '000', additional bible specification
    #     assert BCVID.fromlogos("bible+leb2.19.3.title").ID == "19003000"
    #     # USFM book ID that's not an integer like EpLao
    #     assert BCVID.fromlogos("bible.60.1.1").ID == "C3001001"

    def test_invalid_length(self) -> None:
        """Test that length checks fail correction"""
        with pytest.raises(AssertionError):
            # only 10 chars
            _ = BCVID("4300100100")
        with pytest.raises(AssertionError):
            # 13 chars
            _ = BCVID("4300100100")

    def test_order(self) -> None:
        """Test that order comparisons are correct."""
        assert self.testid == self.testid
        lessid = BCVID("42004001")
        greaterid = BCVID("43001002")
        assert lessid < self.testid
        assert lessid <= self.testid
        assert greaterid > self.testid
        assert greaterid >= self.testid
        assert greaterid != self.testid

    def test_to_usfm(self) -> None:
        """Test to_usfm()."""
        assert self.testid.to_usfm() == "JHN 1:1"
        mrk481 = BCVWPID("410040080011")
        # this drops the word and part indices (by design)
        assert mrk481.to_usfm() == "MRK 4:8"


class TestBCID:
    """Test basic functionality of BCID dataclass."""

    NA1904_ID = "43001"
    testid = BCID(NA1904_ID)

    def test_init(self) -> None:
        """Test initialization and attributes."""
        assert self.testid.book_ID == "43"
        assert self.testid.chapter_ID == "001"
        assert repr(self.testid) == "BCID('43001')"

    # def test_fromusfm(self) -> None:
    #     """Test conversion from USFM-style reference."""
    #     # early OT books should be zero-padded
    #     assert BCID.fromusfm("Gen 3").ID == "01003"
    #     with pytest.raises(AssertionError):
    #         _ = BCID.fromusfm("Genesis 3")
    #     assert BCID.fromusfm("MRK 4").ID == "41004"
    #     with pytest.raises(AssertionError):
    #         _ = BCID.fromusfm("Mark 3")
    # add tests to fail if verse supplied

    # def test_fromlogos(self) -> None:
    #     """Test conversion from Logos-style reference."""
    #     # early OT books should be zero-padded
    #     assert BCID.fromlogos("bible.1.2").ID == "01002"
    #     assert BCID.fromlogos("bible.62.4").ID == "41004"
    #     # USFM book ID that's not an integer like EpLao
    #     assert BCID.fromlogos("bible.60.1").ID == "C3001"
    # add tests to fail if verse supplied

    def test_invalid_length(self) -> None:
        """Test that length checks fail correction"""
        with pytest.raises(AssertionError):
            # too long
            _ = BCID("43001001")
        with pytest.raises(AssertionError):
            # too short
            _ = BCID("4301")

    def test_order(self) -> None:
        """Test that order comparisons are correct."""
        assert self.testid == self.testid
        lessid = BCID("42004")
        greaterid = BCID("43004")
        assert lessid < self.testid
        assert lessid <= self.testid
        assert greaterid > self.testid
        assert greaterid >= self.testid
        assert greaterid != self.testid


class TestBCVWPID:
    """Test basic functionality of BCVWPID dataclass."""

    NA1904_ID = "43001001005"
    testid = BCVWPID(NA1904_ID)

    def test_init(self) -> None:
        """Test initialization and attributes."""
        assert self.testid.book_ID == "43"
        assert self.testid.chapter_ID == "001"
        assert self.testid.verse_ID == "001"
        assert self.testid.word_ID == "005"
        assert self.testid.part_ID == ""
        assert repr(self.testid) == "BCVWPID('43001001005')"

    def test_init_with_part(self) -> None:
        """Test initialization and attributes for an ID with a part."""
        testid = BCVWPID("010020030011")
        assert testid.book_ID == "01"
        assert testid.chapter_ID == "002"
        assert testid.verse_ID == "003"
        assert testid.word_ID == "001"
        assert testid.part_ID == "1"
        assert repr(testid) == "BCVWPID('010020030011')"

    # def test_fromusfm(self) -> None:
    #     """Test conversion from USFM-style reference."""
    #     # early OT books should be zero-padded
    #     assert BCVWPID.fromusfm("Gen 3:16").ID == "01003016000"
    #     with pytest.raises(AssertionError):
    #         _ = BCVWPID.fromusfm("Genesis 3:16")
    #     assert BCVWPID.fromusfm("MRK 4:8").ID == "41004008000"
    #     with pytest.raises(AssertionError):
    #         _ = BCVWPID.fromusfm("Mark 3:16")

    # def test_fromlogos(self) -> None:
    #     """Test conversion from Logos-style reference."""
    #     # early OT books should be zero-padded
    #     assert BCVWPID.fromlogos("bible.1.2.3").ID == "01002003000"
    #     assert BCVWPID.fromlogos("bible.62.4.8").ID == "41004008000"
    #     # 'title' as verse -> '000', additional bible specification
    #     assert BCVWPID.fromlogos("bible+leb2.19.3.title").ID == "19003000000"
    #     # USFM book ID that's not an integer like EpLao
    #     assert BCVWPID.fromlogos("bible.60.1.1").ID == "C3001001000"

    def test_invalid_length(self) -> None:
        """Test that length checks fail correction"""
        with pytest.raises(AssertionError):
            # only 10 chars
            _ = BCVWPID("4300100100")
        with pytest.raises(AssertionError):
            # 13 chars
            _ = BCVWPID("4300100100500")

    # should also test a real part_ID value


class TestSimplify:
    """Test simplify()."""

    mrk4811 = BCVWPID("410040080011")

    def test_simplify(self) -> None:
        """Test simplify()."""
        assert simplify(self.mrk4811, "BID").ID == "41"
        assert simplify(self.mrk4811, "BCID").ID == "41004"
        assert simplify(self.mrk4811, "BCVID").ID == "41004008"
