"""Manage Clear-style identifiers for words and morphology."""


from dataclasses import dataclass, field


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
            USFM numbers (like '40' for Matthew)
        chapter_ID: 3-character string identifying a chapter number
            within the book
        verse_ID: 3-character string identifying the verse number
        word_ID: 3-character string identifying the word number
        part_ID: single character identifying the word part if
            present: only used for Hebrew

    See `books.Books.fromusfmnumber()` for how to convert this number
    to other Book identifiers.

    """

    ID: str
    book_ID: str = field(init=False)
    chapter_ID: str = field(init=False)
    verse_ID: str = field(init=False)
    word_ID: str = field(init=False)
    part_ID: str = ""

    def __post_init__(self) -> None:
        """Compute other values on initialization."""
        assert 12 >= len(self.ID) >= 11, "Invalid length: {self.ID}"
        self.book_ID = self.ID[:2]
        self.chapter_ID = self.ID[2:5]
        self.verse_ID = self.ID[5:8]
        self.word_ID = self.ID[8:11]
        if len(self.ID) == 12:
            self.part_ID = self.ID[11]
            # TODO: add tests, presumably a closed set of values

    def __repr__(self) -> str:
        """Return a string representation."""
        return f"<ClearID: {self.ID}>"
