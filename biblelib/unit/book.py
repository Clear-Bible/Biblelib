"""Define Book class.

Some duplication here with book.book that should be resolved, probably
by migrating that code here.

>>> from biblelib.unit import book
>>> b
Book(identifier='BID('41')')
>>> b.identifier.book_ID
'41'
>>> b.lastchapter
16
>>> b.data
[Chapter(identifier='BCID('41001')'), Chapter(identifier='BCID('41002')'), Chapter(identifier='BCID('41003')'), Chapter(identifier='BCID('41004')'), Chapter(identifier='BCID('41005')'), Chapter(identifier='BCID('41006')'), Chapter(identifier='BCID('41007')'), Chapter(identifier='BCID('41008')'), Chapter(identifier='BCID('41009')'), Chapter(identifier='BCID('41010')'), Chapter(identifier='BCID('41011')'), Chapter(identifier='BCID('41012')'), Chapter(identifier='BCID('41013')'), Chapter(identifier='BCID('41014')'), Chapter(identifier='BCID('41015')'), Chapter(identifier='BCID('41016')')]
>>> b.enumerate(4)
[Chapter(identifier='BCID('41001')'), Chapter(identifier='BCID('41002')'), Chapter(identifier='BCID('41003')'), Chapter(identifier='BCID('41004')')]
>>> b.enumerate(2, 4)
[Chapter(identifier='BCID('41002')'), Chapter(identifier='BCID('41003')'), Chapter(identifier='BCID('41004')')]

"""

from collections import UserDict
from dataclasses import dataclass

# from collections import UserDict
# from csv import DictReader
from pathlib import Path

# from typing import Any

from biblelib.word import BID, BCID
from biblelib import book
from biblelib.unit import Unit, Versification, pad, Chapter, Chapters

UNITPATH = Path(__file__).parent

ALLBOOKS = book.Books()


@dataclass
class BookChapters:
    """Manage a book ID, name, and start/end chapters."""

    book_ID: str
    # BC-format chapter identifiers, including book_ID
    end_ID: str
    start_ID: str = ""
    # redundeant but helpful for debugging
    name: str = ""

    def __post_init__(self) -> None:
        """Compute values after initialization."""
        assert self.start_ID[:2] == self.book_ID, f"start_ID {self.start_ID} does not match book_ID {self.book_ID}"
        assert self.end_ID[:2] == self.book_ID, f"end_ID {self.end_ID} does not match book_ID {self.book_ID}"
        self.bookname = ALLBOOKS.fromusfmnumber(self.book_ID).usfmname
        if self.bookname == "LJE":
            # Letter to Jeremiah starts with chapter 7
            self.start_ID = self.book_ID + "007"
        else:
            # default is chapters start with 1
            self.start_ID = self.book_ID + "001"

    @staticmethod
    def from_book_tuple(booktup: tuple[int, dict[int, int]]) -> "BookChapters":
        """Return a BookChapters instance.

        booktup is like (82, {1: 21, 2: 22, 3: 18}), where 82 is the
        'raw' book index.

        Adjusts numbers to USFM numbering.

        """
        bookindex, chapdict = booktup
        # correct the index: USFM puts DC after protestant canon
        rawbookid = pad(bookindex, count=2)
        usfmbook = ALLBOOKS.fromlogos(f"bible.{rawbookid}")
        bookid = usfmbook.usfmnumber
        # lowest chapter index (see EpJer)
        startindex = min(chapdict.keys())
        startid = pad(startindex, count=3)
        endindex = max(chapdict.keys())
        endid = pad(endindex, count=3)
        return BookChapters(
            book_ID=bookid, name=usfmbook.usfmname, start_ID=(bookid + startid), end_ID=(bookid + endid)
        )

    # @staticmethod
    # def from_chapters_row(row:dict [str, str]) -> "BookChapters":
    #     """Return a BookChapter instance from a row from chapters.tsv."""
    #     return BookChapter()


class AllBookChapters(UserDict):
    """Manage Book and Chapter data.

    Populate by iterating over chapter data.
    """

    chapters = Chapters()

    def __init__(self) -> None:
        """Initialize an instance."""
        super().__init__()
        lastbookid = "00"
        chaps = []
        for chapter_ID, chapverses in self.chapters.items():
            if chapverses.book_ID != lastbookid:
                # a new book: finish the previous one
                self.data[lastbookid] = chaps
                # start a new one
                lastbookid = chapverses.book_ID
                chaps = [Chapter(identifier=BCID(chapter_ID))]
            else:
                chaps.append(Chapter(identifier=BCID(chapter_ID)))
        # finish the last one
        self.data[lastbookid] = chaps


class Book(Unit):
    """Manage Book units (chapters), identified by a 2-char book ID."""

    bookchapters = AllBookChapters()

    def __init__(
        self, list: list = None, identifier: BID = "", versification: Versification = Versification.ENG
    ) -> None:
        """Instantiate a Book.

        - identifier is a BID instance
        """
        super().__init__(list=list, identifier=identifier)
        assert isinstance(identifier, BID), f"Identifier must be a BID instance: {identifier}"
        assert versification in Versification, f"Invalid versification: {versification}"
        self.versification = versification
        self.data = self.bookchapters[self.identifier.book_ID]
        # not right for LJE
        self.lastchapter = len(self.data)
        # self.data = self.enumerate(self.chapverses.lastverse)

    def enumerate(self, arg0: int, arg1: int = 0) -> list[Chapter]:
        """Return a list of chapter instances.

        With two args, interpret as start-1 and stop, unlike range,
        but 1-based (contrary to normal Python indexing), because
        verse numbers are 1-based.
        """
        if not arg1:
            # arg0 is the stopping point
            chaprange = range(arg0)
        else:
            assert arg0 > 0, "0 is not a valid value for arg0"
            chaprange = range(arg0 - 1, arg1)
        return [Chapter(identifier=(BCID(self.identifier.ID + pad(index + 1, count=3)))) for index in chaprange]
