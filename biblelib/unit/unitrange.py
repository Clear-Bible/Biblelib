"""Manage verse range references.

>>> from biblelib.unit import ChapterRange, VerseRange
>>> mrk_2_5 = ChapterRange(start=BCID("41002"), end=BCID("41005"))
>>> mrk_2_5.enumerate()
[BCID('41002'), BCID('41003'), BCID('41004'), BCID('41005')]
>>> onechap = VerseRange(start=BCVID("41001040"), end=BCVID("41002002"))
>>> onechap.enumerate()
[Verse(identifier='BCVID('41001040')'), Verse(identifier='BCVID('41001041')'), ... Verse(identifier='BCVID('41002002')')]


"""

from dataclasses import dataclass, field
from typing import Optional

from biblelib.book import Books
from biblelib.word import BID, BCID, BCVID, simplify
from .chapter import Chapter
from .verse import Verse
from .unit import pad

BOOKS = Books()


# should this test for out-of-range chapters??


@dataclass
class ChapterRange:
    """Manage a range of chapters."""

    startid: BCID
    endid: BCID

    def __post_init__(self) -> None:
        """Check initialization values."""
        assert simplify(self.startid, BID) == simplify(
            self.endid, BID
        ), f"startid {self.startid} and endid (self.endid) must be in the same book."
        assert self.startid <= self.endid, f"Startid {self.startid} must equal or precede endid {self.endid}."

    def enumerate(self) -> list[Chapter]:
        """Return a list of Chapter instances enumerating the chapters in the range.

        Enumerations include the ending Chapter (unlike range).
        """
        if self.startid == self.endid:
            # vacuous range
            return [Chapter(self.startid)]
        else:
            bookid = self.startid.book_ID
            # this assumes chapters are numbered sequentially
            # this may be violated outside the Protestant canon
            startid_chap = int(self.startid.chapter_ID)
            endid_chap = int(self.endid.chapter_ID)
            chapters = list(range(startid_chap, endid_chap + 1))
            return [Chapter(BCID(bookid + pad(i, 3))) for i in chapters]


@dataclass
class VerseRange:
    """Manage a range of verses."""

    startid: BCVID
    endid: BCVID
    # these are computed from startid and endid
    ID: str = field(init=False)
    book: BID = field(init=False)
    # initialized from startid, so could be misleading for
    # cross-chapter ranges
    chapter: BCID = field(init=False)

    def __post_init__(self) -> None:
        """Check initialization values."""
        # enforce typs: a little hacky to change init values like this.
        # It would be less hacky to have a factory method that does this.
        if self.startid.__class__.__name__ != "BCVID":
            self.startid = BCVID(self.startid.to_bcvid)
        if self.endid.__class__.__name__ != "BCVID":
            self.endid = BCVID(self.endid.to_bcvid)
        self.ID = self.startid.ID + "-" + self.endid.ID
        self.book: BID = BID(self.startid.to_bid)
        self.chapter: BCID = BCID(self.startid.to_bcid)
        assert self.book == BID(
            self.endid.to_bid
        ), f"Startid {self.startid} and endid {self.endid} must be in the same book."
        # note this allows a vacuous range with the same start and
        # end: does that make sense?
        assert self.startid <= self.endid, f"Startid {self.startid} must precede endid {self.endid}."

    def __repr__(self) -> str:
        """Return a printed representation."""
        return "<VerseRange: {self.ID}>"

    def enumerate(self) -> list[Verse]:
        """Return a list of Verse instances enumerating the verses in the range.

        Enumerations include the ending Verse value (unlike range).
        """

        def get_verses(bcid: BCID, startindex: int, endindex: int) -> list[Verse]:
            """Return a list of verses."""
            return Chapter(inst=bcid).enumerate(startindex, endindex)

        if self.startid == self.endid:
            # vacuous range
            return [Verse(self.startid)]
        else:
            # this assumes chapters are numbered sequentially
            # this may be violated outside the Protestant canon
            startid_chap_index = int(self.startid.chapter_ID)
            startid_verse_index = int(self.startid.verse_ID)
            endid_chap_index = int(self.endid.chapter_ID)
            endid_verse_index = int(self.endid.verse_ID)
            if startid_chap_index == endid_chap_index:
                chap = Chapter(inst=simplify(self.startid, BCID))
                return chap.enumerate(startid_verse_index, endid_verse_index)
            else:
                # bookid = self.startid.book_ID
                chaprange = ChapterRange(startid=simplify(self.startid, BCID), endid=simplify(self.endid, BCID))
                chapenum = chaprange.enumerate()
                firstbcid = chapenum[0].identifier
                firstchap = Chapter(inst=firstbcid)
                firstverses = get_verses(firstbcid, startid_verse_index, firstchap.lastverse)
                # may be empty
                midbcids: list[Chapter] = chapenum[1:-1]
                # get all verses for any middle chapters
                # WRONG use of get_verses here now that this is a list of Chapters
                midverses = [v for chap in midbcids for v in chap.enumerate(1, chap.lastverse)]
                lastbcid = chapenum[-1].identifier
                # lastchap = Chapter(inst=lastbcid)
                lastverses = get_verses(lastbcid, 1, endid_verse_index)
                return [v for v in (firstverses + midverses + lastverses)]

    def enumerate_ids(self) -> list[BCVID | None]:
        """Return a list of BCVID instances for the range."""
        return [v.inst for v in self.enumerate()]


# I also need WordRange for a sequence of word IDs
def detect_name_range(ref: str) -> str:
    """Return a range instance for a reference.

    Assumes it's called on a reference with a hyphen. Heuristic.

    """
    ref1, ref2 = ref.split("-")
    assert not ("," in ref1 or "," in ref2), f"Can't handle complex range: {ref}"
    namematch = BOOKS.nameregexp.match(ref1)
    assert namematch, f"Invalid name reference: {ref1}"
    bookname, _ = ref1[: namematch.end()], ref1[(namematch.end() + 1) :]
    usfmbook = BOOKS.fromname(bookname).usfmnumber
    if ":" in ref1:
        return f"{usfmbook}, verserange"
    else:
        # match digits
        return f"{usfmbook}, chapterrange"
