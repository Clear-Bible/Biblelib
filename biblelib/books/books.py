"""This module provides utilities for working with Bible book metadata and collections.

This defines canonical sets of Bible books, along with

* standard identifiers, abbreviations, and names
* (forthcoming) the canons that recognize this book, ordered
* (forthcoming) the chapter contents of each book and their final
  verse. This is tradition-specific: Gen 31 has 55 verses in ESV, but
  54 in BHS.


Examples:
    >>> from biblelib import books
    >>> allbooks = books.Books()
    >>> allbooks["MRK"]
    <Book: MRK>
    >>> allbooks["MRK"].osisID
    'Mark'
    >>>
    # retrive a Book instance from an OSIS ID
    >>> allbooks.fromosis("Matt").name
    'Matthew'

See the tests `Biblelib/tests` for additional examples.

To do:

    Add other canons: [Logos' Canon Comparison
    interactive](https://ref.ly/logosres/interactive:canon-comparison?pos=index.html)
    has 14.
    Indicate relations to alternate books, e.g. 'DAN' and 'DAG' (Greek Daniel, which includes other content)?

"""

from collections import UserDict
from csv import DictReader
from dataclasses import dataclass, field
from pathlib import Path
from typing import Union


# This directory: where books.tsv is also located.
BOOKSPATH = Path(__file__).parent


@dataclass
class Book:
    """Dataclass for managing metadata identifying a book from the Bible.

    Typically accessed from Books, which instantiates the full set, or
    subclasses (pending: for a given canon).

    Attributes:
        logosID (int): the index number of this book in the Logos
            bible datatype. Provides a standard ordinal index for
            ordering.
        usfmnumber (str): the USFM string for this book
        usfmname (str): the USFM name for this book
        osisID (str): the OSIS identifier for this book
        name (str): the common English name for this book
        altname (str): a longer or alternate English name, or empty string

    Todo:
        Add canon information.

    """

    # from the Logos bible datatype: some gaps for Ethiopic canon
    # first to support ordinal sorting
    logosID: int
    # despite the name, this is a 2-character string
    usfmnumber: str
    # three characters
    usfmname: str
    osisID: str
    name: str
    altname: str
    _canon_traditions: tuple = ("Catholic", "Jewish", "Protestant")
    # keep this in sync with the attributes below
    _fieldnames: tuple = ("logosID", "usfmnumber", "usfmname", "osisID", "name", "altname")
    # canon-specific
    ordinal: int = field(init=False)

    # - add in JPS sequence numbers for OT books?

    def __repr__(self) -> str:
        """Return a string representation, using USFM name."""
        return f"<Book: {self.usfmname}>"

    def __hash__(self) -> int:
        """Return a hash code.

        Instances are populated with static data, so they're
        functionally immutable (but don't change attribute values!).
        """
        return hash(self.osisID)

    def __eq__(self, o) -> bool:
        """Return True if self is == to other, else False, based on ordinals."""
        return self.ordinal == o.ordinal

    def __ge__(self, o) -> bool:
        """Return True if self is >= other, else False, based on ordinals."""
        return self.ordinal >= o.ordinal

    def __gt__(self, o) -> bool:
        """Return True if self is > other, else False, based on ordinals."""
        return self.ordinal > o.ordinal

    def __le__(self, o) -> bool:
        """Return True if self is <= other, else False, based on ordinals."""
        return self.ordinal <= o.ordinal

    def __lt__(self, o) -> bool:
        """Return True if self is < other, else False, based on ordinals."""
        return self.ordinal < o.ordinal

    @property
    def usfmnumberalt(self) -> str:
        """Return an alternate USFM number, based on Matt="41" rather than "40".

        In some filenames associated with Paratext and legacy data,
        Matt is "41" and subsequent book numbers are one higher,
        through Revelation.  See
        [https://github.com/usfm-bible/tcdocs/issues/3](https://github.com/usfm-bible/tcdocs/issues/3)
        for discussion of this issue.

        Returns:
            a string representing an adjusted USFM number.

        """
        if 87 >= self.logosID >= 61:
            # only affects NT books
            return str(int(self.usfmnumber) + 1)
        else:
            return self.usfmnumber

    def render(self, attrname: str = "osisID") -> str:
        """Return a string rendering the attrname property of Book.

        Args:
            attrname: a dataclass attribute to use for rendering the book.

        Returns:
            str: a rendered representation of Book

        """
        assert attrname in self.__dataclass_fields__, f"Invalid attrname: {attrname}"
        attrval = getattr(self, attrname)
        if attrname == "logosID":
            rendered = f"bible.{attrval}"
        else:
            rendered = attrval
        return rendered

    @property
    def logosURI(self) -> str:
        """Return a URI to open this book in Logos Bible Software in your preferred Bible.

        Example:
            >>> Books()["MRK"].logosURI
            'https://ref.ly/logosref/bible.62'
        """
        return f"https://ref.ly/logosref/{self.render('logosID')}"

    # other URIs to consider
    # YouVersion
    # Bible Gateway
    # Ref.ly? Different Bible book abbreviations, not sure how important


class Books(UserDict):
    """A canonical collection of Bible Book instances."""

    # to add:
    # - Catholic
    # - JPS/Tanakh
    # there are others: LXX? Syriac, Ethiopian, etc.
    source: Path = BOOKSPATH / "books.tsv"
    mappingfields: set = set(Book._fieldnames)
    canon: str = "Protestant"
    logosmap: dict = {}
    osismap: dict = {}
    usfmnaumberap: dict = {}

    def __init__(self, sourcefile: str = "", canon: str = "Protestant") -> None:
        """Initialize a Books instance.

        Instantiates a dict whose keys are 3-character USFM names.

        Args:
            sourcefile: TSV file with book data to load. Canonical
                location is
                https://github.com/Clear-Bible/Biblelib/blob/biblelib/books/books.tsv.
            canon: the canon to use in selecting and ordering books

        """
        super().__init__()
        if sourcefile:
            self.source = Path(sourcefile)
        # need implementation
        if canon != "Protestant":
            raise NotImplementedError("Canon support not yet implemented: default is Protestant.")
        # need smarts here about different canons
        # self.data = [Book(*b) for b in _bookdata]
        with self.source.open(encoding="utf-8") as f:
            # drop comment lines when reading`
            reader: DictReader = DictReader(filter(lambda row: row[0] != "#", f), dialect="excel-tab")
            # make sure the fieldnames in the file are the same as the
            # dataclass attributes
            fieldnameset: set = set(reader.fieldnames[0].split("\t"))
            assert not fieldnameset.difference(
                self.mappingfields
            ), f"Fieldname discrepancy header: {fieldnameset} vs {self.mappingfields}"
            for row in reader:
                # logosID should be an int
                row["logosID"] = int(row["logosID"])
                self.data[row["usfmname"]] = Book(**row)

    def fromlogos(self, logosID: Union[int, str]) -> Book:
        """Return the book instance for a Logos bible book index.

        Args:
            logosID: the Logos identifier to use in looking up the
                Book. Either a datatype reference string like
                'bible.62', or a bare int.
        """
        if isinstance(logosID, str):
            if logosID.startswith("bible."):
                logosID = int(logosID[6:])
            else:
                logosID = int(logosID)
        if not self.logosmap:
            # initialize on demand
            self.logosmap = {b.logosID: b for _, b in self.data.items()}
        return self.logosmap[logosID]

    def fromosis(self, osisID: str) -> Book:
        """Return the book instance for an OSIS identifier.

        Args:
            osisID: the OSIS identifier to use in looking up the Book,
                like "Matt".
        """
        if not self.osismap:
            # initialize on demand
            self.osismap = {b.osisID: b for _, b in self.data.items()}
        return self.osismap[osisID]

    def fromusfmnumber(self, usfmnumber: str) -> Book:
        """Return the book instance for a USFM number.

        Args:
            usfmnumber: the USFM book number to use in looking up the Book,
                like "40".
        """
        if not self.usfmnaumberap:
            # initialize on demand
            self.usfmnaumberap = {b.usfmnumber: b for _, b in self.data.items()}
        return self.usfmnaumberap[usfmnumber]


class _Canon(Books):
    """Return an Books instance representing a specific canon and order."""

    bookids = []

    def __init__(self, *args, **kwargs) -> None:
        """Initialize a Books instance for a Canon."""
        super().__init__(*args, **kwargs)
        # reset the data to only recognized bookids, adding an ordinal
        # for ordering
        srcdata = self.data
        self.data = {}
        for index, bookid in enumerate(self.bookids):
            book = srcdata[bookid]
            book.ordinal = index
            self.data[bookid] = book


class ProtestantCanon(_Canon):
    """Return an Book instance representing the 66-book Protestant canon.

    This does not include the Deuterocanonical books.
    """

    # fmt: off
    bookids = [
        "GEN", "EXO", "LEV", "NUM", "DEU", "JOS", "JDG", "RUT", "1SA", "2SA", "1KI", "2KI", "1CH", "2CH",
        "EZR", "NEH", "EST", "JOB", "PSA", "PRO", "ECC", "SNG", "ISA", "JER", "LAM", "EZK", "DAN",
        "HOS", "JOL", "AMO", "OBA", "JON", "MIC", "NAM", "HAB", "ZEP", "HAG", "ZEC", "MAL",
        "MAT", "MRK", "LUK", "JHN", "ACT", "ROM", "1CO", "2CO", "GAL", "EPH", "PHP", "COL", "1TH", "2TH",
        "1TI", "2TI", "TIT", "PHM", "HEB", "JAS", "1PE", "2PE", "1JN", "2JN", "3JN", "JUD", "REV"]
    # fmt: on


class CatholicCanon(_Canon):
    """Return a  Book instance representing the 73-book Catholic canon.

    This reflects the order in the New American Bible. The order may
    differ in other editions (e.g. Douay-Rheims puts "1MA" and "2MA"
    after "MAL".)

    """

    # fmt: off
    bookids = [
        "GEN", "EXO", "LEV", "NUM", "DEU", "JOS", "JDG", "RUT", "1SA", "2SA", "1KI", "2KI", "1CH", "2CH",
        "EZR", "NEH", "TOB", "JDT", "ESG", "1MA", "2MA",
        "JOB", "PSA", "PRO", "ECC", "SNG", "WIS", "SIR",
        "ISA", "JER", "LAM", "BAR", "EZK",
        # should this be Greek Daniel "DAG"?
        "DAN",
        "HOS", "JOL", "AMO", "OBA", "JON", "MIC", "NAM", "HAB", "ZEP", "HAG", "ZEC", "MAL",
        "MAT", "MRK", "LUK", "JHN", "ACT", "ROM", "1CO", "2CO", "GAL", "EPH", "PHP", "COL", "1TH", "2TH",
        "1TI", "2TI", "TIT", "PHM", "HEB", "JAS", "1PE", "2PE", "1JN", "2JN", "3JN", "JUD", "REV"]
    # fmt: on


# maybe subclass Books for specific canons??
