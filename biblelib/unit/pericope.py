"""Define Pericope class.

Pericopes are like chapters in that they include a sequence of
verses. However, unlike chapters:
- they don't have conventional identifiers, and don't fit the BCV
  scheme.
- they reflect an analysis: they're not standardized

Design:
- pericope analysis are loaded from a TSV file
- pericopes are simply numbered in sequence for a book to produce an identifier
- pericopes define start and end points with BCV notation.
- pericopes have a title
- pericopes can generate their included verses (ideally with lazy loading)

>>> from biblelib.unit import pericope
# how many pericopes in all?
>>> len(pericope.Pericopes())
1459
>>> pericope.Pericope.pericopes["66022"]
PericopeVerses(pericope_ID="66022", end_ID="66022021")
# what's the last verse of Rev 22 ("66022")?
>>> pericope.Pericope.pericopes["66022"].lastverse
21
>>> pericope.Pericope.books["REV"]
<Book: REV>
# instantiate a Pericope instance for Jude pericope 1. Note the
# identifier must be a BCID instance
>>> jude_1 = pericope.Pericope(identifier=pericope.BCID("65001"))
>>> jude_1
Pericope(identifier=BCID('65001'))
>>> jude_1.parent
{'Book': <Book: JUD>}
>>> jude_1.book_ID
'65'
# enumerate the first four verses in the pericope
>>> jude_1.enumerate(4)
[Verse(identifier='BCVID('65001001')'), Verse(identifier='BCVID('65001002')'), Verse(identifier='BCVID('65001003')'), Verse(identifier='BCVID('65001004')')]
# enumerate verses 2-4
>>> jude_1.enumerate(2, 4)
[Verse(identifier='BCVID('65001002')'), Verse(identifier='BCVID('65001003')'), Verse(identifier='BCVID('65001004')')]
# enumerate all the verses in the pericope
>>> jude_1.enumerate(jude_1.lastverse)
[Verse(identifier='BCVID('65001001')'), Verse(identifier='BCVID('65001002')'), Verse(identifier='BCVID('65001003')'), Verse(identifier='BCVID('65001004')'), Verse(identifier='BCVID('65001005')'), Verse(identifier='BCVID('65001006')'), Verse(identifier='BCVID('65001007')'), Verse(identifier='BCVID('65001008')'), Verse(identifier='BCVID('65001009')'), Verse(identifier='BCVID('65001010')'), Verse(identifier='BCVID('65001011')'), Verse(identifier='BCVID('65001012')'), Verse(identifier='BCVID('65001013')'), Verse(identifier='BCVID('65001014')'), Verse(identifier='BCVID('65001015')'), Verse(identifier='BCVID('65001016')'), Verse(identifier='BCVID('65001017')'), Verse(identifier='BCVID('65001018')'), Verse(identifier='BCVID('65001019')'), Verse(identifier='BCVID('65001020')'), Verse(identifier='BCVID('65001021')'), Verse(identifier='BCVID('65001022')'), Verse(identifier='BCVID('65001023')'), Verse(identifier='BCVID('65001024')'), Verse(identifier='BCVID('65001025')')]

"""

from collections import UserDict
from csv import DictReader
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from biblelib.word import BCID, BCVID
from biblelib import book
from .unit import Unit, Versification, pad
from .verse import Verse

UNITPATH = Path(__file__).parent

ALLBOOKS = book.Books()


@dataclass
class PericopeVerses:
    """Manage a book ID, pericope ID, and end verses.

    First verse is always assumed to be 1.
    """

    # BC-format pericope identifier: includes book_ID
    pericope_ID: str
    end_ID: str
    book_ID: str = ""
    lastverse: int = 0
    _fields: tuple = ("pericope_ID", "end_ID")

    def __post_init__(self) -> None:
        """Compute values after initialization."""
        self.book_ID = self.pericope_ID[:2]
        # should be a better way
        try:
            self.lastverse = int(self.end_ID[5:])
        except Exception as e:
            print(f"Failed setting lastverse with {self.end_ID}={self.end_ID}\n{e}")

    def __repr__(self) -> str:
        """Return a printed instance."""
        return f'{self.__class__.__name__}(pericope_ID="{self.pericope_ID}", end_ID="{self.end_ID}")'

    @staticmethod
    def get_pericopeverses(bookindex: str, pericopeindex: str, lastverse: str) -> "PericopeVerses":
        """Return a PericopeVerses instance.

        Inputs are
        - bookindex: an integer from the Logos sequence (MAT == 61)
        - pericopeindex: a pericope integer (1-based)
        - endindex: the integer of the last verse in the pericope (1-based)
        """
        # correct the index: USFM puts DC after protestant canon
        usfmbook = ALLBOOKS.fromlogos(f"bible.{bookindex}")
        bookid = usfmbook.usfmnumber
        pericope_ID = bookid + pad(pericopeindex, count=3)
        end_ID = pericope_ID + pad(lastverse, count=3)
        return PericopeVerses(pericope_ID=pericope_ID, end_ID=end_ID)


class Pericopes(UserDict):
    """Manage pericope verse data."""

    def __init__(self, pericopeversesfile: str = "pericopeverses.tsv") -> None:
        """Initialize a collection of pericope verse data.

        Keys are BCID values, values are PericopeVerses instances.
        """
        super().__init__()
        with (UNITPATH / pericopeversesfile).open() as f:
            reader = DictReader(f, fieldnames=PericopeVerses._fields, delimiter="\t")
            # skip the header
            next(reader)
            self.data = {bcid: PericopeVerses(**row) for row in reader if (bcid := row["pericope_ID"])}
            # does not handle LJE correctly: only one pericope, indexed as 6


# TODO: cache these
class Pericope(Unit):
    """Manage Pericope units.

    The scheme for identifying pericopes is BC (no verse, word or part index):
    these identifiers are used for comparison.

    A versification attribute indicates how the identifiers should be
    interpreted: only the default of the 'eng' scheme for now, and not
    actually used yet.

    """

    _books = book.Books()
    _pericopes = Pericopes()
    # if defined, the parent instance: e.g. parent_pericope of Mark 4:3 is Mark 4
    # could also be parent sentence, paragraph, pericope ... so dict for extensibility
    parent: dict[str, Any] = {"Book": None}

    def __init__(
        self, list: list = None, identifier: BCID = "", versification: Versification = Versification.ENG
    ) -> None:
        """Instantiate a Pericope.

        - identifier is a BCID instance
        """
        super().__init__(list=list, identifier=identifier)
        assert isinstance(identifier, BCID), f"Identifier must be a BCID instance: {identifier}"
        assert versification in Versification, f"Invalid versification: {versification}"
        self.versification = versification
        # populate with verse instances
        self.book_ID = self.identifier.book_ID
        self.parent["Book"] = self._books.fromusfmnumber(self.book_ID)
        self.parentbook = self.parent["Book"]
        self.book_usfmname = self.parentbook.usfmname
        # assumes the first verse of every pericope has index 1: fragile
        self.chapverses: PericopeVerses = self._pericopes[self.identifier.ID]
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
        return [Verse(identifier=(BCVID(self.identifier.ID + pad(index + 1, count=3)))) for index in verserange]
