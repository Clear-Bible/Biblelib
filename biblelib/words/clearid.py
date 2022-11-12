"""Manage Clear-style identifiers for words and morphology.

ToDo:
    provide for references without word IDs, or even without chapter IDs?

"""


from dataclasses import dataclass, field
import re

from biblelib.books import Books

BOOKS = Books()


def pad3(arg: str) -> str:
    """Return a zero-padded string for an integer.

    "title" is verse 0, so there's possible confusion with unspecified
    verses vs. titles specified as 000.

    """
    if arg == "title":
        return "000"
    else:
        assert len(arg) <= 3, f"Arg must be 3 chars or less: {arg}"
        assert int(arg), f"Arg must convert to an int: {arg}"
        return "{:03}".format(int(arg))


@dataclass
class ClearID:
    """Identifies words from Bible texts by book, chapter, verse, ord, and word part.

    This supports two formats: BBCCCVVVWWW and BBCCCVVVWWWP, where BB
        identifies a book, CCC identifies a chapter number, VVV
        identifies a verse number, and WWW identifies a word number
        within that verse. If P is present it identifies a word part:
        this is only used for Hebrew.

    This dataclass does not validate whether any identifiers are in
    the correct range: it only records the data. Use TBD for
    validation.

    Attributes:
        book_ID: 2-character string identifying the Bible book using
            USFM numbers (like '40' for Matthew, 'B7' for Enoch)
        chapter_ID: 3-character string identifying a chapter number
            within the book
        verse_ID: 3-character string identifying the verse number
        word_ID: 3-character string identifying the word number
        part_ID: single character identifying the word part if
            present: only used for Hebrew

    See `books.Books.fromusfmnumber()` for how to convert this number
    to other Book identifiers.

    """

    # book mapping data
    ID: str
    book_ID: str = field(init=False)
    chapter_ID: str = field(init=False)
    verse_ID: str = field(init=False)
    word_ID: str = field(init=False)
    part_ID: str = ""

    def __post_init__(self) -> None:
        """Compute other values on initialization."""
        assert 12 >= len(self.ID) >= 11, f"Invalid length: {self.ID}"
        self.book_ID = self.ID[0:2]
        self.chapter_ID = self.ID[2:5]
        self.verse_ID = self.ID[5:8]
        self.word_ID = self.ID[8:11]
        if len(self.ID) == 12:
            self.part_ID = self.ID[12]
            # TODO: add tests, presumably a closed set of values

    def __repr__(self) -> str:
        """Return a string representation."""
        return f"<ClearID: {self.ID}>"

    @staticmethod
    def fromusfm(ref) -> "ClearID":
        """Return a ClearID instance for a USFM-based reference.

        Only handles single verse references with a specified chapter
        and verse like MRK 4:8. Does not handle ranges, book + chapter
        references, or non-numeric verses like 'title'. Does not check
        the validity of chapter and verse numbers for the book.

        """
        book, chapter, verse = re.split(r"[: ]", ref, maxsplit=2)
        # could be more generous here in matching other abbreviation
        # schemes as well
        assert book.upper() in BOOKS, f"Invalid book abbreviation: {book}"
        usfmbook = BOOKS[book.upper()].usfmnumber
        assert int(chapter), f"Chapter must be an integer: {chapter}"
        assert int(verse), f"Verse must be an integer: {verse}"
        return ClearID(f"{usfmbook}{pad3(chapter)}{pad3(verse)}000")

    @staticmethod
    def fromlogos(ref) -> "ClearID":
        """Return a ClearID instance for a Logos-style single verse reference."""
        if ref.startswith("bible") and "." in ref:
            bible, restref = ref.split(".", 1)
        else:
            restref = ref
        # eventually we may need to handle different Bible versions
        refsplit = restref.split(".")
        assert len(refsplit) == 3, f"Invalid reference: {restref}"
        # convert e.g. 62 -> "41" (Logos -> USFM), and 1 -> "01"
        usfmbook = BOOKS.fromlogos(refsplit[0]).usfmnumber
        chapter = pad3(refsplit[1])
        verse = pad3(refsplit[2])
        # append "00" for word
        return ClearID(f"{usfmbook}{chapter}{verse}000")
