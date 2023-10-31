"""Manage verse range references.

>>> mrk_2_5 = ChapterRange(start=BCID("41002"), end=BCID("41005"))
>>> mrk_2_5.enumerate()
[BCID('41002'), BCID('41003'), BCID('41004'), BCID('41005')]
>>> onechap = range.VerseRange(start=BCVID("41001040"), end=BCVID("41002002"))
>>> onechap.enumerate()
[Verse(identifier='BCVID('41001040')'), Verse(identifier='BCVID('41001041')'), ... Verse(identifier='BCVID('41002002')')]


"""


from dataclasses import dataclass

from biblelib.word import BID, BCID, BCVID, simplify
from biblelib.unit import Chapter, Verse, pad

# should this test for out-of-range chapters??


@dataclass
class ChapterRange:
    """Manage a range of chapters."""

    start: BCID
    end: BCID

    def __post_init__(self) -> None:
        """Check initialization values."""
        assert simplify(self.start, BID) == simplify(
            self.end, BID
        ), f"Start {self.start} and end (self.end) must be in the same book."
        assert self.start <= self.end, f"Start {self.start} must precede end {self.end}."

    def enumerate(self) -> list[BCID]:
        """Return a list of BCID instances enumerating the chapters in the range.

        Enumerations include the end value (unlike range).
        """
        if self.start == self.end:
            # vacuous range
            return [self.start]
        else:
            bookid = self.start.book_ID
            # this assumes chapters are numbered sequentially
            # this may be violated outside the Protestant canon
            start_chap = int(self.start.chapter_ID)
            end_chap = int(self.end.chapter_ID)
            chapters = list(range(start_chap, end_chap + 1))
            return [BCID(bookid + pad(i, 3)) for i in chapters]


@dataclass
class VerseRange:
    """Manage a range of verses."""

    start: BCVID
    end: BCVID

    def __post_init__(self) -> None:
        """Check initialization values."""
        assert simplify(self.start, BID) == simplify(
            self.end, BID
        ), f"Start {self.start} and end (self.end) must be in the same book."
        assert self.start <= self.end, f"Start {self.start} must precede end {self.end}."

    def enumerate(self) -> list[BCVID]:
        """Return a list of BCVID instances enumerating the verses in the range.

        Enumerations include the end value (unlike range).
        """

        def get_verses(bcid: BCID, startindex: int, endindex: int) -> list[Verse]:
            """Return a list of verses."""
            return Chapter(inst=bcid).enumerate(startindex, endindex)

        if self.start == self.end:
            # vacuous range
            return [self.start]
        else:
            # this assumes chapters are numbered sequentially
            # this may be violated outside the Protestant canon
            start_chap_index = int(self.start.chapter_ID)
            start_verse_index = int(self.start.verse_ID)
            end_chap_index = int(self.end.chapter_ID)
            end_verse_index = int(self.end.verse_ID)
            if start_chap_index == end_chap_index:
                chap = Chapter(inst=simplify(self.start, BCID))
                return chap.enumerate(start_verse_index, end_verse_index)
            else:
                # bookid = self.start.book_ID
                chaprange = ChapterRange(start=simplify(self.start, BCID), end=simplify(self.end, BCID))
                chapenum = chaprange.enumerate()
                firstbcid = chapenum[0]
                firstchap = Chapter(inst=firstbcid)
                firstverses = get_verses(firstbcid, start_verse_index, firstchap.lastverse)
                # may be empty
                midbcids = chapenum[1:-1]
                # get all verses for any middle chapters
                midverses = [
                    v for bcid in midbcids if (chap := Chapter(inst=bcid)) for v in get_verses(bcid, 1, chap.lastverse)
                ]
                lastbcid = chapenum[-1]
                lastchap = Chapter(inst=lastbcid)
                lastverses = get_verses(lastbcid, 1, end_verse_index)
                return firstverses + midverses + lastverses
