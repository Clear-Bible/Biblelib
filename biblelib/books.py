"""Utilities for working with Bible books.

This defines canonical sets of Bible books, along with
- standard identifiers, abbreviations, and names
- (forthcoming) the chapter contents of each book and their final verse
- (forthcoming) the canons that recognize this book

Usage:

>>> from biblelib import books
>>> allbooks = books.Books()
>>> allbooks[40]
Book(usfmnumber='42', usfmname='MRK', osisID='Mark', clearID='', logosID=62, name='Mark', altname='The Gospel according to Mark', n_chapters=16)
>>> allbooks[40].osisID
'Mark'

# retrive a Book instance from an OSIS ID
>>> allbooks.fromosis("Matt")
Book(usfmnumber='41', usfmname='MAT', osisID='Matt', clearID='', logosID=61, name='Matthew', altname='The Gospel according to Matthew', n_chapters=28)
>>> allbooks.fromosis("Matt").name
'Matthew'
>>> allbooks.fromosis("Matt").n_chapters
28

See ../tests/test_books.py for additional examples.

"""

from collections import UserList
from dataclasses import dataclass


# Data from https://ubsicap.github.io/usfm/identification/books.html
# - Logos Bible datatype number. This supports ordinal sorting
#   according to Protestant canon order. Other orders need other support.
# - USFM Number (but really a string)
# - USFM Identifier
# - OSIS ID
# - Clear ID
# - English Name
# - Long English Name
# - number of chapters
# Numerous alternate names in other canons are not included
# Order of items here must match properties in Book for loading to
# work correctly

_bookdata = (
    (1, "01", "GEN", "Gen", "gn", "Genesis", "", 50),
    (2, "02", "EXO", "Exod", "ex", "Exodus", "", 40),
    (3, "03", "LEV", "Lev", "lv", "Leviticus", "", 27),
    (4, "04", "NUM", "Num", "nu", "Numbers", "", 36),
    (5, "05", "DEU", "Deut", "dt", "Deuteronomy", "", 34),
    (6, "06", "JOS", "Josh", "js", "Joshua", "", 24),
    (7, "07", "JDG", "Judg", "ju", "Judges", "", 21),
    (8, "08", "RUT", "Ruth", "ru", "Ruth", "", 4),
    (9, "09", "1SA", "1Sam", "1s", "1 Samuel", "", 31),
    (10, "10", "2SA", "2Sam", "2s", "2 Samuel", "", 24),
    (11, "11", "1KI", "1Kgs", "1k", "1 Kings", "", 22),
    (12, "12", "2KI", "2Kgs", "2k", "2 Kings", "", 25),
    (13, "13", "1CH", "1Chr", "1c", "1 Chronicles", "", 29),
    (14, "14", "2CH", "2Chr", "2c", "2 Chronicles", "", 36),
    (15, "15", "EZR", "Ezra", "er", "Ezra", "", 10),
    (16, "16", "NEH", "Neh", "ne", "Nehemiah", "", 13),
    (17, "17", "EST", "Esth", "es", "Esther (Hebrew)", "", 10),
    (18, "18", "JOB", "Job", "jb", "Job", "", 42),
    (19, "19", "PSA", "Ps", "ps", "Psalms", "", 150),
    (20, "20", "PRO", "Prov", "pr", "Proverbs", "", 31),
    (21, "21", "ECC", "Eccl", "ec", "Ecclesiastes", "", 12),
    (22, "22", "SNG", "Song", "ca", "Song of Songs", "Song of Solomon", 8),
    (23, "23", "ISA", "Isa", "is", "Isaiah", "", 66),
    (24, "24", "JER", "Jer", "je", "Jeremiah", "The Book of Jeremiah", 52),
    (25, "25", "LAM", "Lam", "lm", "Lamentations", "The Lamentations of Jeremiah", 5),
    (26, "26", "EZK", "Ezek", "ek", "Ezekiel", "", 48),
    (27, "27", "DAN", "Dan", "da", "Daniel", "", 12),
    (28, "28", "HOS", "Hos", "ho", "Hosea", "", 14),
    (29, "29", "JOL", "Joel", "jl", "Joel", "", 4),
    (30, "30", "AMO", "Amos", "am", "Amos", "", 9),
    (31, "31", "OBA", "Obad", "ob", "Obadiah", "", 1),
    (32, "32", "JON", "Jonah", "jn", "Jonah", "", 4),
    (33, "33", "MIC", "Mic", "mi", "Micah", "", 7),
    (34, "34", "NAM", "Nah", "na", "Nahum", "", 3),
    (35, "35", "HAB", "Hab", "hb", "Habakkuk", "", 3),
    (36, "36", "ZEP", "Zeph", "zp", "Zephaniah", "", 3),
    (37, "37", "HAG", "Hag", "hg", "Haggai", "", 2),
    (38, "38", "ZEC", "Zech", "zc", "Zechariah", "", 14),
    (39, "39", "MAL", "Mal", "ma", "Malachi", "", 3),
    # unclear if MAT should be 40 or 41
    (61, "41", "MAT", "Matt", "", "Matthew", "The Gospel according to Matthew", 28),
    (62, "42", "MRK", "Mark", "", "Mark", "The Gospel according to Mark", 16),
    (63, "43", "LUK", "Luke", "", "Luke", "The Gospel according to Luke", 24),
    (64, "44", "JHN", "John", "", "John", "The Gospel according to John", 21),
    (65, "45", "ACT", "Acts", "", "Acts", "The Acts of the Apostles", 28),
    (66, "46", "ROM", "Rom", "", "Romans", "The Letter of Paul to the Romans", 16),
    (67, "47", "1CO", "1Cor", "", "1 Corinthians", "The First Letter of Paul to the Corinthians", 16),
    (68, "48", "2CO", "2cor", "", "2 Corinthians", "The Second Letter of Paul to the Corinthians", 13),
    (69, "49", "GAL", "Gal", "", "Galatians", "The Letter of Paul to the Galatians", 6),
    (70, "50", "EPH", "Eph", "", "Ephesians", "The Letter of Paul to the Ephesians", 6),
    (71, "51", "PHP", "Phil", "", "Philippians", "The Letter of Paul to the Philippians", 4),
    (72, "52", "COL", "Col", "", "Colossians", "The Letter of Paul to the Colossians", 4),
    (73, "53", "1TH", "1Thess", "", "1 Thessalonians", "The First Letter of Paul to the Thessalonians", 5),
    (74, "54", "2TH", "2Thess", "", "2 Thessalonians", "The Second Letter of Paul to the Thessalonians", 3),
    (75, "55", "1TI", "1Tim", "", "1 Timothy", "The First Letter of Paul to Timothy", 6),
    (76, "56", "2TI", "2Tim", "", "2 Timothy", "The Second Letter of Paul to Timothy", 4),
    (77, "57", "TIT", "Titus", "", "Titus", "The Letter of Paul to Titus", 3),
    (78, "58", "PHM", "Phlm", "", "Philemon", "The Letter of Paul to Philemon", 1),
    (79, "59", "HEB", "Heb", "", "Hebrews", "The Letter to the Hebrews", 13),
    (80, "60", "JAS", "Jas", "", "James", "The Letter of James", 5),
    (81, "61", "1PE", "1Pet", "", "1 Peter", "The First Letter of Peter", 5),
    (82, "62", "2PE", "2Pet", "", "2 Peter", "The Second Letter of Peter", 3),
    (83, "63", "1JN", "1John", "", "1 John", "The First Letter of John", 5),
    (84, "64", "2JN", "2John", "", "2 John", "The Second Letter of John", 1),
    (85, "65", "3JN", "3John", "", "3 John", "The Third Letter of John", 1),
    (86, "66", "JUD", "Jude", "", "Jude", "The Letter of Jude", 1),
    (87, "67", "REV", "Rev", "", "Revelation", "The Revelation to John", 22),
    # ("68", "TOB", 40, "Tobit", ""),
    # ("69", "JDT", 41, "Judith", ""),
    # ("70", "ESG", 42, "Esther Greek", ""),
    # ("71", "WIS", 43, "Wisdom of Solomon", ""),
    # ("72", "SIR", 44, "Sirach", "Ecclesiasticus"),
    # ("73", "BAR", 45, "Baruch", ""),
    # ("74", "LJE", 46, "Letter of Jeremiah", ""),
    # ("75", "S3Y", 47, "Song of the 3 Young Men", ""),
    # ("76", "SUS", 48, "Susanna", ""),
    # ("77", "BEL", 49, "Bel and the Dragon", ""),
    # ("78", "1MA", 50, "1 Maccabees", ""),
    # ("79", "2MA", 51, "2 Maccabees", ""),
    # ("80", "3MA", 55, "3 Maccabees", ""),
    # ("81", "4MA", 57, "4 Maccabees", ""),
    # ("82", "1ES", 52, "1 Esdras (Greek)", ""),
    # ("83", "2ES", 56, "2 Esdras (Latin)", ""),
    # ("84", "MAN", 53, "Prayer of Manasseh", ""),
    # ("85", "PS2", 54, "Psalm 151", ""),
    # ("86", "ODA", 58, "Odae/Odes", ""),
    # ("87", "PSS", 59, "Psalms of Solomon", ""),
    # ("A4", "EZA", 100, "Ezra Apocalypse", ""),
    # # no Logos number AFAIK: numbered from 900
    # ("A5", "5EZ", 900, "5 Ezra", ""),
    # ("A6", "6EZ", 901, "6 Ezra", ""),
    # ("B2", "DAG", 98, "Daniel Greek", ""),
    # ("B3", "PS3", 902, "Psalms 152-155", ""),
    # ("B4", "2BA", 96, "2 Baruch (Apocalypse)", "The Apocalypse of Baruch"),
    # ("B5", "LBA", 97, "Letter of Baruch", ""),
    # ("B6", "JUB", 903, "Jubilees", ""),
    # ("B7", "ENO", 88, "Enoch", ""),
    # ("B8", "1MQ", 904, "1 Meqabyan/Mekabis", "Book of Mekabis of Benjamin"),
    # ("B9", "2MQ", 905, "2 Meqabyan/Mekabis", "Book of Mekabis of Moab"),
    # ("C0", "3MQ", 906, "3 Meqabyan/Mekabis", "Book of Meqabyan"),
    # ("C1", "REP", 907, "Reproof", ""),
    # ("C2", "4BA", 908, "4 Baruch", ""),
    # ("C3", "LAO", 60, "Letter to the Laodiceans", ""),
)


@dataclass(order=True)
class Book:
    """Information about a book from the Bible.

    Typically accessed from Books, which instantiates the full set
    (pending: for a given canon).

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
    # internal Clear standard?
    clearID: str
    name: str
    altname: str
    n_chapters: int

    # add __post_init__
    # - add in JPS sequence numbers for OT books?

    def __hash__(self) -> int:
        """Return a hash code.

        Instances are populated with static data, so they're
        functionally immutable (but don't change attribute values!).
        """
        return hash(self.osisID)

    def render(self, attrname: str = "osisID") -> str:
        """Return a string rendering the attrname property of Book."""
        assert attrname in self.__dataclass_fields__, f"Invalid attrname: {attrname}"
        attrval = getattr(self, attrname)
        if attrname == "logosID":
            rendered = f"bible.{attrval}"
        else:
            rendered = attrval
        return rendered


class Books(UserList):
    """A canonical collection of Bible books."""

    canon: str = "Protestant"
    osismap: dict = {}
    usfmnamemap: dict = {}

    def __init__(self, canon: str = "Protestant") -> None:
        """Initialize a Books instance."""
        # need implementation
        if canon != "Protestant":
            raise NotImplementedError("Canon support not yet implemented: default is Protestant.")
        # need smarts here about different canons
        self.data = [Book(*b) for b in _bookdata]

    def fromosis(self, osisID: str):
        """Return the book for an OSIS ID."""
        if not self.osismap:
            # initialize on demand
            self.osismap = {b.osisID: b for b in self.data}
        return self.osismap[osisID]

    def fromusfmname(self, usfmname: str):
        """Return the book for a USFM name."""
        if not self.usfmnamemap:
            # initialize on demand
            self.usfmnamemap = {b.usfmname: b for b in self.data}
        return self.usfmnamemap[usfmname]
