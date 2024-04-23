"""Define Chapter class.

>>> from biblelib.unit import chapter
# how many chapters in all?
>>> len(chapter.Chapters())
1459
>>> chapter.Chapter.chapters["66022"]
ChapterVerses(chapter_ID="66022", end_ID="66022021")
# what's the last verse of Rev 22 ("66022")?
>>> chapter.Chapter.chapters["66022"].lastverse
21
>>> chapter.Chapter.books["REV"]
<Book: REV>
# instantiate a Chapter instance for Jude chapter 1. Note the
# identifier must be a BCID instance
>>> jude_1 = chapter.Chapter(identifier=chapter.BCID("65001"))
>>> jude_1
Chapter(identifier=BCID('65001'))
>>> jude_1.parent
{'Book': <Book: JUD>}
>>> jude_1.book_ID
'65'
# enumerate the first four verses in the chapter
>>> jude_1.enumerate(4)
[Verse(identifier='BCVID('65001001')'), Verse(identifier='BCVID('65001002')'), Verse(identifier='BCVID('65001003')'), Verse(identifier='BCVID('65001004')')]
# enumerate verses 2-4
>>> jude_1.enumerate(2, 4)
[Verse(identifier='BCVID('65001002')'), Verse(identifier='BCVID('65001003')'), Verse(identifier='BCVID('65001004')')]
# enumerate all the verses in the chapter
>>> jude_1.enumerate(jude_1.lastverse)
[Verse(identifier='BCVID('65001001')'), Verse(identifier='BCVID('65001002')'), Verse(identifier='BCVID('65001003')'), Verse(identifier='BCVID('65001004')'), Verse(identifier='BCVID('65001005')'), Verse(identifier='BCVID('65001006')'), Verse(identifier='BCVID('65001007')'), Verse(identifier='BCVID('65001008')'), Verse(identifier='BCVID('65001009')'), Verse(identifier='BCVID('65001010')'), Verse(identifier='BCVID('65001011')'), Verse(identifier='BCVID('65001012')'), Verse(identifier='BCVID('65001013')'), Verse(identifier='BCVID('65001014')'), Verse(identifier='BCVID('65001015')'), Verse(identifier='BCVID('65001016')'), Verse(identifier='BCVID('65001017')'), Verse(identifier='BCVID('65001018')'), Verse(identifier='BCVID('65001019')'), Verse(identifier='BCVID('65001020')'), Verse(identifier='BCVID('65001021')'), Verse(identifier='BCVID('65001022')'), Verse(identifier='BCVID('65001023')'), Verse(identifier='BCVID('65001024')'), Verse(identifier='BCVID('65001025')')]

"""

from collections import UserDict
from csv import DictReader
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Union

from biblelib.word import BCID, BCVID, BCVWPID, simplify, reftypes
from biblelib import book
from .unit import Unit, Versification, pad
from .verse import Verse

UNITPATH = Path(__file__).parent

ALLBOOKS = book.Books()


@dataclass
class ChapterVerses:
    """Manage a book ID, chapter ID, and end verses.

    First verse is always assumed to be 1.
    """

    # BC-format chapter identifier: includes book_ID
    chapter_ID: str
    end_ID: str
    book_ID: str = ""
    lastverse: int = 0
    _fields: tuple = ("chapter_ID", "end_ID")

    def __post_init__(self) -> None:
        """Compute values after initialization."""
        self.book_ID = self.chapter_ID[:2]
        # should be a better way
        try:
            self.lastverse = int(self.end_ID[5:])
        except Exception as e:
            print(f"Failed setting lastverse with {self.end_ID}={self.end_ID}\n{e}")

    def __repr__(self) -> str:
        """Return a printed instance."""
        return f'{self.__class__.__name__}(chapter_ID="{self.chapter_ID}", end_ID="{self.end_ID}")'

    @staticmethod
    def get_chapterverses(bookindex: str, chapterindex: str, lastverse: str) -> "ChapterVerses":
        """Return a ChapterVerses instance.

        Inputs are
        - bookindex: an integer from the Logos sequence (MAT == 61)
        - chapterindex: a chapter integer (1-based)
        - endindex: the integer of the last verse in the chapter (1-based)
        """
        # correct the index: USFM puts DC after protestant canon
        usfmbook = ALLBOOKS.fromlogos(f"bible.{bookindex}")
        bookid = usfmbook.usfmnumber
        chapter_ID = bookid + pad(int(chapterindex), count=3)
        end_ID = chapter_ID + pad(int(lastverse), count=3)
        return ChapterVerses(chapter_ID=chapter_ID, end_ID=end_ID)


class Chapters(UserDict):
    """Manage chapter verse data."""

    def __init__(self, chapterversesfile: str = "chapterverses.tsv") -> None:
        """Initialize a collection of chapter verse data.

        Keys are BCID values, values are ChapterVerses instances.
        """
        super().__init__()
        with (UNITPATH / chapterversesfile).open() as f:
            reader = DictReader(f, fieldnames=ChapterVerses._fields, delimiter="\t")
            # skip the header
            next(reader)
            self.data = {bcid: ChapterVerses(**row) for row in reader if (bcid := row["chapter_ID"])}
            # does not handle LJE correctly: only one chapter, indexed as 6


# TODO: cache these
# parameter names here are confusing: "identifier" is really an
# instance of BCID, etc., and for the superclass it needs comparison
# methods
class Chapter(Unit):
    """Manage Chapter units.

    The scheme for identifying chapters is BC (no verse, word or part index):
    these identifiers are used for comparison.

    A versification attribute indicates how the identifiers should be
    interpreted: only the default of the 'eng' scheme for now, and not
    actually used yet.

    """

    _books = book.Books()
    _chapters = Chapters()
    # if defined, the parent instance: e.g. parent_chapter of Mark 4:3 is Mark 4
    # could also be parent sentence, paragraph, pericope ... so dict for extensibility
    # parent: dict[str, Any] = {}  # {"Book": None}

    def __init__(
        self,
        inst: Union[BCID, BCVID, BCVWPID],
        initlist: Optional[list] = None,
        versification: Versification = Versification.ENG,
    ) -> None:
        """Instantiate a Chapter.

        - inst is a BCID instance
        """
        # not sure how to silence the type complaint hre
        self.inst: reftypes = simplify(inst, BCID)
        super().__init__(initlist=initlist, identifier=self.inst)
        assert versification in Versification, f"Invalid versification: {versification}"
        self.versification = versification
        # populate with verse instances
        self.book_ID = self.inst.book_ID
        self.parent["Book"] = self._books.fromusfmnumber(self.book_ID)
        self.parentbook = self.parent["Book"]
        self.book_usfmname = self.parentbook.usfmname
        # assumes the first verse of every chapter has index 1: fragile
        self.chapverses: ChapterVerses = self._chapters[self.inst.ID]
        self.lastverse = self.chapverses.lastverse
        self.data = self.enumerate(self.chapverses.lastverse)

    def enumerate(self, arg0: int, arg1: int = 0) -> list[Verse]:
        """Return a list of verse instances.

        With two args, interpret as start-1 and stop, unlike range,
        but 1-based (contrary to normal Python indexing), because
        verse numbers are 1-based.
        """
        if not arg1:
            # arg0 is the stopping point
            verserange = range(arg0)
        else:
            assert arg0 > 0, "0 is not a valid value for arg0"
            verserange = range(arg0 - 1, arg1)
        return [Verse(inst=(BCVID(self.inst.ID + str(index + 1).zfill(3)))) for index in verserange]
