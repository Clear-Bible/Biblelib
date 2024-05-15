"""Test biblelib.word.bcvwpid."""

import typing

import pytest

from biblelib.word import BID, BCID, BCVID, BCVIDRange, BCVWPID
from biblelib.word import fromlogos, fromname, fromosis, fromusfm, fromubs, simplify, to_bcv

from biblelib.word.bcvwpid import pad3


class TestPad3:
    """Test basic functionality of pad3()."""

    def test_return(self) -> None:
        """Test returned values"""
        assert pad3("title") == "000"
        assert pad3("0") == "000"
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
        assert fromname("Psalm") == BID("19")
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
        assert fromosis("Gen.2") == BCID("01002")
        assert fromosis("Gen.12") == BCID("01012")
        assert fromosis("Ps.119") == BCID("19119")
        assert fromosis("Mark.4") == BCID("41004")

    def test_fromosis_chapter_verse(self) -> None:
        """Test returned values"""
        assert fromosis("Gen.2.3") == BCVID("01002003")
        assert fromosis("Gen.12.10") == BCVID("01012010")
        assert fromosis("Ps.119.1") == BCVID("19119001")
        assert fromosis("Mark.4.1") == BCVID("41004001")


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


class TestFromUBS:
    """Test basic functionality of fromubs()."""

    def test_from_ubs(self) -> None:
        """Test returned values"""
        assert fromubs("02306000600008") == [BCVWPID("23060006004")]
        assert fromubs("02306000600008{N:001}") == [BCVWPID("23060006004")]
        assert fromubs("02306000600008({N:001})") == [BCVWPID("23060006004")]
        assert fromubs("04100400300008") == [BCVWPID("41004003004")]
        assert fromubs("04100400300008") == [BCVWPID("41004003004")]
        # verse-level reference returns BCVID
        assert fromubs("00100301500000") == [BCVID("01003015")]
        assert fromubs("04100400900000") == [BCVID("41004009")]
        with pytest.raises(AssertionError):
            # missing leading zero
            assert fromubs("4100401800000") == [BCVID("41004009")]

    @pytest.mark.filterwarnings("ignore:Invalid book ID for MARBLE ID")
    def test_from_ubs_warnings(self) -> None:
        """Test returned values from from_ubs()."""
        # DC reference returns empty list
        assert fromubs("07300102100020") == []


class TestBID:
    """Test basic functionality of BID dataclass."""

    genid = "01"
    markid = "41"

    def test_init(self) -> None:
        """Test initialization and attributes."""
        assert BID(self.genid).book_ID == self.genid
        assert BID(self.markid).book_ID == self.markid
        # defined on the superclass
        assert BID(self.markid).to_bid == self.markid

    def test_hash(self) -> None:
        """Ensure hashable.

        Values are mysteriously different, but this test seems
        ... ok.

        """
        assert isinstance(BID(self.markid), typing.Hashable)

    def test_includes(self) -> None:
        """Test includes operator."""
        mark = BID(self.markid)
        assert mark.includes(mark)
        assert mark.includes(BCID("41004"))
        assert mark.includes(BCVID("41004008"))
        assert mark.includes(BCVWPID("410040080011"))
        assert not mark.includes(BID("40"))
        assert not mark.includes(BCID("40001"))
        assert not mark.includes(BCVID("40001001"))
        assert not mark.includes(BCVWPID("400010010011"))


class TestBCID:
    """Test basic functionality of BCID dataclass."""

    NA1904_ID = "43001"
    testid = BCID(NA1904_ID)

    def test_init(self) -> None:
        """Test initialization and attributes."""
        assert self.testid.book_ID == "43"
        assert self.testid.chapter_ID == "001"
        assert repr(self.testid) == "BCID('43001')"
        assert self.testid.to_bid == "43"
        assert self.testid.to_bcid == self.NA1904_ID

    def test_hash(self) -> None:
        """Ensure hashable.

        Values are mysteriously different, but this test seems
        ... ok.

        """
        assert isinstance(self.testid, typing.Hashable)

    def test_includes(self) -> None:
        """Test includes operator."""
        mark4 = BCID("41004")
        assert mark4.includes(mark4)
        assert mark4.includes(BCVID("41004008"))
        assert mark4.includes(BCVWPID("410040080011"))
        assert not mark4.includes(BCID("40001"))
        assert not mark4.includes(BCVID("40001001"))
        assert not mark4.includes(BCVWPID("400010010011"))

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
        assert self.testid.to_bid == "43"
        assert self.testid.to_bcid == "43001"
        assert self.testid.to_bcvid == self.NA1904_ID
        assert self.testid.get_id() == self.NA1904_ID

    def test_hash(self) -> None:
        """Ensure hashable.

        Values are mysteriously different, but this test seems
        ... ok.

        """
        assert isinstance(self.testid, typing.Hashable)

    def test_includes(self) -> None:
        """Test includes operator."""
        mark4_8 = BCVID("41004008")
        assert mark4_8.includes(mark4_8)
        assert mark4_8.includes(BCVWPID("410040080011"))
        assert not mark4_8.includes(BCVID("41001001"))
        assert not mark4_8.includes(BCVID("40001001"))
        assert not mark4_8.includes(BCVWPID("400010010011"))

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


class TestBCVIDRange:
    """Test basic functionality of BCVWPRange dataclass."""

    mark4_8 = BCVID("41004008")
    mark4_13 = BCVID("41004013")
    markrange = BCVIDRange(mark4_8, mark4_13)

    def test_init(self) -> None:
        """Test initialization and attributes."""
        assert self.markrange.startid == self.mark4_8
        assert self.markrange.endid == self.mark4_13
        assert repr(self.markrange) == "BCVIDRange('41004008-41004013')"
        assert self.markrange.ID == "41004008-41004013"
        assert self.markrange.book == BID("41")
        assert self.markrange.chapter == BCID("41004")
        assert self.markrange.end_chapter == BCID("41004")

    def test_enumerate(self) -> None:
        """Test enumerate()."""
        assert self.markrange.enumerate() == [
            BCVID("41004008"),
            BCVID("41004009"),
            BCVID("41004010"),
            BCVID("41004011"),
            BCVID("41004012"),
            BCVID("41004013"),
        ]
        # vacuous range
        assert BCVIDRange(self.mark4_8, BCVID("41004008")).enumerate() == [BCVID("41004008")]
        # no cross-chapter ranges yet
        with pytest.raises(NotImplementedError):
            # not implemented
            _ = BCVIDRange(BCVID("41004008"), BCVID("41005001")).enumerate()


class TestBCVWPID:
    """Test basic functionality of BCVWPID dataclass."""

    NA1904_ID = "43001001005"
    testid = BCVWPID(NA1904_ID)

    def test_init(self) -> None:
        """Test initialization and attributes."""
        assert self.testid.canon_prefix == "n"
        assert self.testid.book_ID == "43"
        assert self.testid.chapter_ID == "001"
        assert self.testid.verse_ID == "001"
        assert self.testid.word_ID == "005"
        assert self.testid.part_ID == "1"
        assert self.testid.get_id(part_index=False) == "43001001005"
        assert repr(self.testid) == "BCVWPID('430010010051')"

    def test_init_with_part(self) -> None:
        """Test initialization and attributes for an ID with a part."""
        genid = BCVWPID("010020030011")
        assert genid.canon_prefix == "o"
        assert genid.book_ID == "01"
        assert genid.chapter_ID == "002"
        assert genid.verse_ID == "003"
        assert genid.word_ID == "001"
        assert genid.part_ID == "1"
        assert repr(genid) == "BCVWPID('010020030011')"

    def test_init_with_prefix(self) -> None:
        """Test initialization and attributes for an ID with a prefix."""
        testid = BCVWPID("o010020030011")
        assert testid.canon_prefix == "o"
        assert testid.book_ID == "01"
        assert testid.chapter_ID == "002"
        assert testid.verse_ID == "003"
        assert testid.word_ID == "001"
        assert testid.part_ID == "1"

    def test_hash(self) -> None:
        """Ensure hashable.

        Values are mysteriously different, but this test seems
        ... ok.

        """
        assert isinstance(self.testid, typing.Hashable)

    def test_get_id(self) -> None:
        """Test get_id()."""
        gen = BCVWPID("010010010051")
        assert gen.get_id() == "010010010051"
        assert gen.get_id(prefix=True) == "o010010010051"
        # this wouldn't make sense for Hebrew, but ...
        assert gen.get_id(part_index=False) == "01001001005"
        assert self.testid.get_id() == "430010010051"
        assert self.testid.get_id(prefix=True) == "n430010010051"
        assert self.testid.get_id(part_index=False) == "43001001005"
        assert self.testid.get_id(prefix=True, part_index=False) == "n43001001005"
        # should also test "x" canon prefix

    def test_includes(self) -> None:
        """Test includes operator."""
        testid = BCVWPID("010020030011")
        assert testid.includes(testid)
        assert not testid.includes(BCVWPID("400010010011"))

    def test_invalid_length(self) -> None:
        """Test that length checks fail correction"""
        with pytest.raises(AssertionError):
            # only 10 chars
            _ = BCVWPID("4300100100")
        with pytest.raises(AssertionError):
            # 13 chars
            _ = BCVWPID("4300100100500")

    def test_id(self) -> None:
        """Test various id properties."""
        assert self.testid.to_bid == "43"
        assert self.testid.to_bcid == "43001"
        assert self.testid.to_bcvid == "43001001"

    # should also test a real part_ID value


class TestSimplify:
    """Test simplify()."""

    mrk4811 = BCVWPID("410040080011")

    def test_simplify_BCID(self) -> None:
        """Test simplify()."""
        mrk4 = BCID("41004")
        assert simplify(mrk4, BID).ID == "41"

    def test_simplify_BCVID(self) -> None:
        """Test simplify()."""
        mrk48 = BCVID("41004008")
        assert simplify(mrk48, BID).ID == "41"
        assert simplify(mrk48, BCID).ID == "41004"

    def test_simplify_BCVWPID(self) -> None:
        """Test simplify()."""
        assert simplify(self.mrk4811, BID).ID == "41"
        assert simplify(self.mrk4811, BCID).ID == "41004"
        assert simplify(self.mrk4811, BCVID).ID == "41004008"


class TestTo_bcv:
    """Test to_bcv()."""

    def test_to_bcv_bcvinst(self) -> None:
        """Test to_bcv()."""
        assert to_bcv(BCVID("41004003")) == "41004003"

    def test_to_bcv_bcvwpinst(self) -> None:
        """Test to_bcv()."""
        assert to_bcv(BCVWPID("n41004003001")) == "41004003"
        assert to_bcv(BCVWPID("n410040030011")) == "41004003"
        assert to_bcv(BCVWPID("41004003001")) == "41004003"
        with pytest.raises(AssertionError):
            # missing word index
            assert to_bcv(BCVWPID("n41004003")) == "41004003"

    def test_to_bcv_str(self) -> None:
        """Test to_bcv()."""
        # macula canon prefixes are not supported here
        assert to_bcv("n41004003001") == "41004003"
