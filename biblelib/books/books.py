"""Utilities for working with Bible books.

This defines canonical sets of Bible books, along with
- standard identifiers, abbreviations, and names
- (forthcoming) the canons that recognize this book, ordered
- (forthcoming) the chapter contents of each book and their final
  verse. This is tradition-specific: Gen 31 has 55 verses in ESV, but
  54 in BHS.


Usage:

>>> from biblelib import books
>>> allbooks = books.Books()
>>> allbooks[61]
<Book: Mark>
>>> allbooks[61].osisID
'Mark'

# retrive a Book instance from an OSIS ID
>>> allbooks.fromosis("Matt").name
'Matthew'

See ../tests/test_books.py for additional examples.

"""

from collections import UserList
from csv import DictReader
from dataclasses import dataclass
from pathlib import Path
from typing import Union


# Data from https://ubsicap.github.io/usfm/identification/books.html
# - Logos Bible datatype number. This supports ordinal sorting
#   according to Protestant canon order. Other orders need other support.
# - USFM Number (but really a string)
# - USFM Identifier
# - OSIS ID
# - 'standard' English Name
# - Long English Name
# - number of chapters

# Numerous alternate names in other canons are not included
# Order of items here must match properties in Book for loading to
# work correctly

# Excluded by design:
# - Different published Bibles have different names for books
#   (e.g. 1SA is "1 Kings" in Douay-Rheims). So 'name' here is a -
#   conventional one: more data would be required to capture published
#   names in other editions.
# - Some Clear data has a two-letter abbreviation, perhaps originating
#   with Andi Wu (Gen = "gn", Lev = "lx", etc. ). Non-normative so excluded

_bookdata = (
    (1, "01", "GEN", "Gen", "Genesis", "", 50),
    (2, "02", "EXO", "Exod", "Exodus", "", 40),
    (3, "03", "LEV", "Lev", "Leviticus", "", 27),
    (4, "04", "NUM", "Num", "Numbers", "", 36),
    (5, "05", "DEU", "Deut", "Deuteronomy", "", 34),
    (6, "06", "JOS", "Josh", "Joshua", "", 24),
    (7, "07", "JDG", "Judg", "Judges", "", 21),
    (8, "08", "RUT", "Ruth", "Ruth", "", 4),
    (9, "09", "1SA", "1Sam", "1 Samuel", "", 31),
    (10, "10", "2SA", "2Sam", "2 Samuel", "", 24),
    (11, "11", "1KI", "1Kgs", "1 Kings", "", 22),
    (12, "12", "2KI", "2Kgs", "2 Kings", "", 25),
    (13, "13", "1CH", "1Chr", "1 Chronicles", "", 29),
    (14, "14", "2CH", "2Chr", "2 Chronicles", "", 36),
    (15, "15", "EZR", "Ezra", "Ezra", "", 10),
    (16, "16", "NEH", "Neh", "Nehemiah", "", 13),
    (17, "17", "EST", "Esth", "Esther (Hebrew)", "", 10),
    (18, "18", "JOB", "Job", "Job", "", 42),
    (19, "19", "PSA", "Ps", "Psalms", "", 150),
    (20, "20", "PRO", "Prov", "Proverbs", "", 31),
    (21, "21", "ECC", "Eccl", "Ecclesiastes", "", 12),
    (22, "22", "SNG", "Song", "Song of Songs", "Song of Solomon", 8),
    (23, "23", "ISA", "Isa", "Isaiah", "", 66),
    (24, "24", "JER", "Jer", "Jeremiah", "The Book of Jeremiah", 52),
    (25, "25", "LAM", "Lam", "Lamentations", "The Lamentations of Jeremiah", 5),
    (26, "26", "EZK", "Ezek", "Ezekiel", "", 48),
    (27, "27", "DAN", "Dan", "Daniel", "", 12),
    (28, "28", "HOS", "Hos", "Hosea", "", 14),
    (29, "29", "JOL", "Joel", "Joel", "", 4),
    (30, "30", "AMO", "Amos", "Amos", "", 9),
    (31, "31", "OBA", "Obad", "Obadiah", "", 1),
    (32, "32", "JON", "Jonah", "Jonah", "", 4),
    (33, "33", "MIC", "Mic", "Micah", "", 7),
    (34, "34", "NAM", "Nah", "Nahum", "", 3),
    (35, "35", "HAB", "Hab", "Habakkuk", "", 3),
    (36, "36", "ZEP", "Zeph", "Zephaniah", "", 3),
    (37, "37", "HAG", "Hag", "Haggai", "", 2),
    (38, "38", "ZEC", "Zech", "Zechariah", "", 14),
    (39, "39", "MAL", "Mal", "Malachi", "", 3),
    # gap in the USFM numbering sequence here because of the legacy
    # issue of MAT as 41 rather than 40.
    (40, "68", "TOB", "Tob", "Tobit", "", 0),
    (41, "69", "JDT", "Jdt", "Judith", "", 0),
    (42, "70", "ESG", "EsthGr", "Esther Greek", "", 0),
    (43, "71", "WIS", "Wis", "Wisdom of Solomon", "", 0),
    (44, "72", "SIR", "Sir", "Sirach", "Ecclesiasticus", 0),
    (45, "73", "BAR", "Bar", "Baruch", "", 0),
    (46, "74", "LJE", "EpJer", "Letter of Jeremiah", "", 0),
    (47, "75", "S3Y", "PrAzar", "Song of the 3 Young Men", "", 0),
    (48, "76", "SUS", "Sus", "Susanna", "", 0),
    (49, "77", "BEL", "Bel", "Bel and the Dragon", "", 0),
    (50, "78", "1MA", "1Macc", "1 Maccabees", "", 0),
    (51, "79", "2MA", "2Macc", "2 Maccabees", "", 0),
    (52, "82", "1ES", "1Esd", "1 Esdras (Greek)", "", 0),
    (53, "84", "MAN", "PrMan", "Prayer of Manasseh", "", 0),
    (54, "85", "PS2", "AddPs", "Psalm 151", "", 0),
    (55, "80", "3MA", "3Macc", "3 Maccabees", "", 0),
    (56, "83", "2ES", "2Esd", "2 Esdras (Latin)", "", 0),
    (57, "81", "4MA", "4Macc", "4 Maccabees", "", 0),
    (58, "86", "ODA", "Odes", "Odae/Odes", "", 0),
    (59, "87", "PSS", "PssSol", "Psalms of Solomon", "", 0),
    (60, "C3", "LAO", "EpLao", "Letter to the Laodiceans", "", 0),
    # Some filenames and legacy data have USFM number for MAT as 41,
    # and +1 for subsequent NT books: use usfmnumberalt for that. But
    # most common current practice is MAT = 40.
    (61, "40", "MAT", "Matt", "Matthew", "The Gospel according to Matthew", 28),
    (62, "41", "MRK", "Mark", "Mark", "The Gospel according to Mark", 16),
    (63, "42", "LUK", "Luke", "Luke", "The Gospel according to Luke", 24),
    (64, "43", "JHN", "John", "John", "The Gospel according to John", 21),
    (65, "44", "ACT", "Acts", "Acts", "The Acts of the Apostles", 28),
    (66, "45", "ROM", "Rom", "Romans", "The Letter of Paul to the Romans", 16),
    (67, "46", "1CO", "1Cor", "1 Corinthians", "The First Letter of Paul to the Corinthians", 16),
    (68, "47", "2CO", "2cor", "2 Corinthians", "The Second Letter of Paul to the Corinthians", 13),
    (69, "48", "GAL", "Gal", "Galatians", "The Letter of Paul to the Galatians", 6),
    (70, "49", "EPH", "Eph", "Ephesians", "The Letter of Paul to the Ephesians", 6),
    (71, "50", "PHP", "Phil", "Philippians", "The Letter of Paul to the Philippians", 4),
    (72, "51", "COL", "Col", "Colossians", "The Letter of Paul to the Colossians", 4),
    (73, "52", "1TH", "1Thess", "1 Thessalonians", "The First Letter of Paul to the Thessalonians", 5),
    (74, "53", "2TH", "2Thess", "2 Thessalonians", "The Second Letter of Paul to the Thessalonians", 3),
    (75, "54", "1TI", "1Tim", "1 Timothy", "The First Letter of Paul to Timothy", 6),
    (76, "55", "2TI", "2Tim", "2 Timothy", "The Second Letter of Paul to Timothy", 4),
    (77, "56", "TIT", "Titus", "Titus", "The Letter of Paul to Titus", 3),
    (78, "57", "PHM", "Phlm", "Philemon", "The Letter of Paul to Philemon", 1),
    (79, "58", "HEB", "Heb", "Hebrews", "The Letter to the Hebrews", 13),
    (80, "59", "JAS", "Jas", "James", "The Letter of James", 5),
    (81, "60", "1PE", "1Pet", "1 Peter", "The First Letter of Peter", 5),
    (82, "61", "2PE", "2Pet", "2 Peter", "The Second Letter of Peter", 3),
    (83, "62", "1JN", "1John", "1 John", "The First Letter of John", 5),
    (84, "63", "2JN", "2John", "2 John", "The Second Letter of John", 1),
    (85, "64", "3JN", "3John", "3 John", "The Third Letter of John", 1),
    (86, "65", "JUD", "Jude", "Jude", "The Letter of Jude", 1),
    (87, "66", "REV", "Rev", "Revelation", "The Revelation to John", 22),
    (88, "B7", "ENO", "1En", "Enoch", "", 0),
    # Logos also has 2 Baruch (99)??
    # LBD: "The Syriac Apocalypse of Baruch proper consists of 2
    # Baruch 1–77, while 2 Baruch 78–87 form the Letter of Baruch."
    # I'm guessing USFM doesn't distinguish?
    (96, "B4", "2BA", "2Bar", "2 Baruch (Apocalypse)", "The Apocalypse of Baruch", 0),
    (97, "B5", "LBA", "EpBar", "Letter of Baruch", "", 0),
    (98, "B2", "DAG", "DanGr", "Daniel Greek", "", 0),
    # (99, "2 Baruch"),
    (100, "A4", "EZA", "4Ezra", "Ezra Apocalypse", "", 0),
    # # no Logos number AFAIK: arbitrarily numbered from 200
    (200, "A5", "5EZ", "5Ezra", "5 Ezra", "", 0),
    (201, "A6", "6EZ", "6Ezra", "6 Ezra", "", 0),
    (202, "B3", "PS3", "5ApocSyrPss", "Psalms 152-155", "", 0),
    (203, "B6", "JUB", "Jub", "Jubilees", "", 0),
    (204, "B8", "1MQ", "1Meq", "1 Meqabyan/Mekabis", "Book of Mekabis of Benjamin", 0),
    (205, "B9", "2MQ", "2Meq", "2 Meqabyan/Mekabis", "Book of Mekabis of Moab", 0),
    (206, "C0", "3MQ", "3Meq", "3 Meqabyan/Mekabis", "Book of Meqabyan", 0),
    (207, "C1", "REP", "Rep", "Reproof", "", 0),
    (208, "C2", "4BA", "4Bar", "4 Baruch", "", 0),
    # more from Logos, per
    # https://wiki.logos.com/Logos_Bible_Book_Names, but not in
    # USFM/OSIS? These seems to be from DSS5
    # `logosref:bibleNN` doesn't navigate for more in Logos for NN > 87
    # (89, "Plea for Deliverance"),
    # (90, "Apostrophe to Zion"),
    # (91, "Eschatalogical Hymn"),
    # (92, "Apostrophe to Judah"),
    # (93, "Hymn to the Creator"),
    # (94, "David's Compositions"),
    # (95, "Apocryphal Psalms"),
    # (101, "Catena"),
    # (102, "Psalm 151A"),
    # (103, "Psalm 151B"),
)


@dataclass(order=True)
class Book:
    """Dataclass with information about a book from the Bible.

    Typically accessed from Books, which instantiates the full set, or
    subclasses (pending: for a given canon).

    Attributes:
    - logosID: the index number of this book in the Logos bible
      datatype. Provides a standard ordinal index for ordering.
    - usfmnumber: the USFM string for this book
    - usfmname: the USFM name for this book
    - osisID: the OSIS identifier for this book
    - name: the common English name for this book
    - altname: a longer or alternate English name

    Todo:
    - Add chapter and canon information.
    """

    _canon_traditions = tuple(["Catholic", "Jewish", "Protestant"])
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
    n_chapters: int

    # add __post_init__
    # - add in JPS sequence numbers for OT books?

    def __repr__(self) -> str:
        """Return a string representation, using OSIS ID."""
        return f"<Book: {self.osisID}>"

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

        Examples:
            # assumes book is instantiated to Matthew
            >>> book.render()
            'Matt'
            >>> book.render('usfmname')
            'MAT'

        """
        assert attrname in self.__dataclass_fields__, f"Invalid attrname: {attrname}"
        attrval = getattr(self, attrname)
        if attrname == "logosID":
            rendered = f"bible.{attrval}"
        else:
            rendered = attrval
        return rendered


class Books(UserList):
    """A canonical collection of Bible books."""

    # to add:
    # - Catholic
    # - JPS/Tanakh
    # there are others: LXX? Syriac, Ethiopian, etc.
    source: Path = Path("../../../macula-greek/sources/Clear/mappings/mappings-GNT-stripped.tsv")
    mappingfields: list = list(Book.__dataclass_fields__.keys())
    canon: str = "Protestant"
    logosmap: dict = {}
    osismap: dict = {}
    usfmnamemap: dict = {}

    def __init__(self, canon: str = "Protestant") -> None:
        """Initialize a Books instance.

        Args:
            canon (str): the canon to use in selecting and ordering books
        """
        # need implementation
        if canon != "Protestant":
            raise NotImplementedError("Canon support not yet implemented: default is Protestant.")
        # need smarts here about different canons
        # self.data = [Book(*b) for b in _bookdata]
        with self.source.open(encoding="utf-8") as f:
            reader: DictReader = DictReader(f, dialect="excel-tab")
            # make sure the fieldnames in the file are the same as the
            # dataclass attributes
            fieldnameset: set = set(reader.fieldnames[0].split("\t"))
            assert not fieldnameset.difference(
                self.mappingfields
            ), f"Fieldname discrepancy header: {fieldnameset} vs {self.mappingfields}"
            self.data: list = [Book(**r) for r in reader]

    def fromlogos(self, logosID: Union[int, str]) -> Book:
        """Return the book for a Logos bible book index.

        Args:
            logosID (str or int): the Logos identifier to use in
                looking up the Book. Either a datatype reference
                string like 'bible.62', or a bare int.

        Returns:
            a Book instance.

        Examples:
            >>> Books().fromlogos("bible.62")
            <Book: Mark>

        """
        if isinstance(logosID, str):
            if logosID.startswith("bible."):
                logosID = int(logosID[6:])
            else:
                logosID = int(logosID)
        if not self.logosmap:
            # initialize on demand
            self.logosmap = {b.logosID: b for b in self.data}
        return self.logosmap[logosID]

    def fromosis(self, osisID: str) -> Book:
        """Return the book for an OSIS identifier.

        Args:
        - osisID (str): the OSIS identifier to use in looking up the
          Book, like "Matt".

        Returns:
        - a Book instance.
        """
        if not self.osismap:
            # initialize on demand
            self.osismap = {b.osisID: b for b in self.data}
        return self.osismap[osisID]

    def fromusfmname(self, usfmname: str) -> Book:
        """Return the book for a USFM name.

        Args:
        - usfmname (str): the USFM name to use in looking up the
          Book, like "MATT".

        Returns:
        - a Book instance.
        """
        if not self.usfmnamemap:
            # initialize on demand
            self.usfmnamemap = {b.usfmname: b for b in self.data}
        return self.usfmnamemap[usfmname.upper()]


# maybe subclass Books for specific canons??
