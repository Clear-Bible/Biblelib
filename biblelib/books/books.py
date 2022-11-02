"""Utilities for working with Bible books.

This defines canonical sets of Bible books, along with
- standard identifiers, abbreviations, and names
- (forthcoming) the canons that recognize this book, ordered
- (forthcoming) the chapter contents of each book and their final
  verse. This is tradition-specific: Gen 31 has 55 verses in ESV, but
  54 in BHS.


Examples:
>>> from biblelib import books
>>> allbooks = books.Books("biblelib/books/books.tsv")
>>> allbooks["MRK"]
<Book: MRK>
>>> allbooks["MRK"].osisID
'Mark'

# retrive a Book instance from an OSIS ID
>>> allbooks.fromosis("Matt").name
'Matthew'

See ../tests/test_books.py for additional examples.

"""

from collections import UserDict
from csv import DictReader
from dataclasses import dataclass
from pathlib import Path
from typing import Union


@dataclass(order=True)
class Book:
    """Dataclass with information about a book from the Bible.

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

    @property
    def usfmnumberalt(self) -> str:
        """Return an alternate USFM number, based on Matt="41".

        In some filenames associated with Paratext and legacy data,
        Matt is "41" and subsequent book numbers are one higher.  See
        https://github.com/usfm-bible/tcdocs/issues/3 for discussion
        of this issue.

        Returns:
            int: an adjusted USFM number

        """
        if 87 >= self.logosID >= 61:
            # only affects NT books
            return str(int(self.usfmnumber) + 1)
        else:
            return self.usfmnumber

    def render(self, attrname: str = "osisID") -> str:
        """Return a string rendering the attrname property of Book.

        Args:
            attrname (str): a dataclass attribute to use for rendering the book.

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
        """Return a URI to open this book in Logos in your preferred Bible."""
        return f"https://ref.ly/logosref/{self.render('logosID')}"

    # other URIs to consider
    # YouVersion
    # Bible Gateway
    # Ref.ly? Different Bible book abbreviations, not sure how important


class Books(UserDict):
    """A canonical collection of Bible books."""

    # to add:
    # - Catholic
    # - JPS/Tanakh
    # there are others: LXX? Syriac, Ethiopian, etc.
    source: Path = Path("books.tsv")
    mappingfields: set = set(Book._fieldnames)
    canon: str = "Protestant"
    logosmap: dict = {}
    osismap: dict = {}
    usfmnamemap: dict = {}

    def __init__(self, sourcefile: str = "", canon: str = "Protestant") -> None:
        """Initialize a Books instance.

        Instantiates a dict whose keys are 3-character USFM names.

        Args:
            sourcefile (str): TSV file with book data to load
            canon (str): the canon to use in selecting and ordering books
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
        """Return the book for a Logos bible book index.

        Args:
            logosID (str or int): the Logos identifier to use in
                looking up the Book. Either a datatype reference
                string like 'bible.62', or a bare int.

        Returns:
            a Book instance.

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
        """Return the book for an OSIS identifier.

        Args:
            osisID (str): the OSIS identifier to use in looking up the
          Book, like "Matt".

        Returns:
            a Book instance.
        """
        if not self.osismap:
            # initialize on demand
            self.osismap = {b.osisID: b for _, b in self.data.items()}
        return self.osismap[osisID]


# maybe subclass Books for specific canons??
