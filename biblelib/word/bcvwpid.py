"""Manage BCVWP identifiers for words and morphology.

Technically, this should be called BBCCCVVVWWWP format, but that's a
mouthful.

BCVWP = Book, Chapter, Verse, Word, Part as sequential numerical
indices. This is typically encoded as BBCCCVVVWWWP, but there are
variants: sometimes the Part index is omitted. Individual Bible
editions might have different text indexed in different ways, so you
should not assume that BCVWP value for one Bible maps directly to another.

>>> from biblelib.word import BCVID, BCVWPID
>>> bcv = BCVID("41004003")
>>> bcv.book_ID
"41"
>>> bcv.chapter_ID
"004"
>>> bcv.verse_ID
"003"
>>> bcv < BCVID("41005001")
True
>>> BCVID.fromusfm("Gen 3:16")
BCVID("01003016")
>>> BCVID.fromlogos("bible.1.2.3")
BCVID("01002003")

Similar things work with BCID (book and chapter) and BCVWPID.

ToDo:
- add a containment hierarchy:
    - BID().includes(BCVID()) -> bool
    - BID().includes(BCVWPID()) (because of transitivity)
    - maybe just treat this internally as substring matching?
- rewrite with pydantic?
- one set of `from_X` methods that return the right kind of instance
  depending on the number of characters
- figure out whether this is a case for composition (rather than
  subclassing)
- methods for rendering in various formats

"""


from dataclasses import dataclass, field
from typing import Union

from biblelib.book import Books

BOOKS = Books()


@dataclass(order=True)
class BID:
    """Identifies a book identifier.

    Also a base class for other BCV identifiers.
    """

    # book mapping data
    ID: str
    book_ID: str = field(init=False)
    # the longth of the book portion of an ID
    _idlen: int = 2

    def __post_init__(self) -> None:
        """Compute other values on initialization."""
        assert len(self.ID) == 2, f"length should be 2 characters: {self.ID}"
        self.book_ID = self.ID
        # also test that they're all digits, in the right range, etc.

    def __repr__(self) -> str:
        """Return a string representation."""
        return f"{type(self).__name__}('{self.ID}')"

    # this could go in a base class
    # can't reference B*ID types until defined :-/
    def includes(self, other: str) -> bool:
        """Return True if other is included in the scope of self.

        Simply based on substring matching. Any instance includes
        itself therefore.

        """
        assert (
            isinstance(other, BID)
            or isinstance(other, BCID)
            or isinstance(other, BCVID)
            # or isinstance(other, BCVWID)
            or isinstance(other, BCVWPID)
        ), f"Invalid type with includes(): {other}"
        return other.ID[: self._idlen].startswith(self.ID)

    def to_usfm(self) -> str:
        """Return a USFM representation."""
        usfmbook = BOOKS.fromusfmnumber(self.book_ID).usfmname
        return f"{usfmbook}"

    # @staticmethod
    # def fromusfm(ref) -> "BID":
    #     """Return a BID instance for a USFM-based book name."""
    #     assert ref.upper() in BOOKS, f"Invalid book abbreviation: {ref}"
    #     usfmbook = BOOKS[ref.upper()].usfmnumber
    #     return BID(usfmbook)

    # @staticmethod
    # def fromlogos(ref) -> "BID":
    #     """Return a BID instance for a Logos-style book reference."""
    #     if ref.startswith("bible") and "." in ref:
    #         bible, restref = ref.split(".", 1)
    #     else:
    #         restref = ref
    #     usfmbook = BOOKS.fromlogos(restref).usfmnumber
    #     return BID(usfmbook)


@dataclass(order=True)
class BCVID:
    """Identifies book, chapter, verse from Bible texts.

    This supports the format BBCCCVVV, where BB identifies a book,
        CCC identifies a chapter number, and VVV identifies a verse.

    This dataclass does not validate whether any identifiers are in
    the correct range: it only records the data. Use <TBD> for
    validation. All sequence indices are one-based, not zero-based.

    Attributes:
        book_ID: 2-character string identifying the Bible book using
            USFM numbers (like '40' for Matthew, 'B7' for Enoch)
        chapter_ID: 3-character string identifying a chapter number
            within the book
        verse_ID: 3-character string identifying the verse number

    See `books.Books.fromusfmnumber()` for how to convert this number
    to other Book identifiers.

    """

    # book mapping data
    ID: str
    book_ID: str = field(init=False)
    chapter_ID: str = field(init=False)
    verse_ID: str = field(init=False)
    # the longth of the book+chapter+verse portion of an ID
    _idlen = 8

    def __post_init__(self) -> None:
        """Compute other values on initialization."""
        assert len(self.ID) == 8, f"length should be 8 characters: {self.ID}"
        self.book_ID = self.ID[0:2]
        self.chapter_ID = self.ID[2:5]
        self.verse_ID = self.ID[5:8]
        # also test that they're all digits, in the right range, etc.

    def __repr__(self) -> str:
        """Return a string representation."""
        return f"{type(self).__name__}('{self.ID}')"

    def includes(self, other: str) -> bool:
        """Return True if other is included in the scope of self.

        Simply based on substring matching. Any instance includes
        itself therefore.

        """
        assert (
            isinstance(other, BCVID)
            # or isinstance(other, BCVWID)
            or isinstance(other, BCVWPID)
        ), f"Invalid type with includes(): {other}"
        return other.ID[: self._idlen].startswith(self.ID)

    def to_usfm(self) -> str:
        """Return a USFM representation."""
        usfmbook = BOOKS.fromusfmnumber(self.book_ID).usfmname
        return f"{usfmbook} {int(self.chapter_ID)}:{int(self.verse_ID)}"

    # @staticmethod
    # def fromusfm(ref) -> "BCVID":
    #     """Return a BCVID instance for a USFM-based reference.

    #     Only handles single verse references with a specified chapter
    #     and verse like MRK 4:8. Does not handle ranges, book + chapter
    #     references, or non-numeric verses like 'title'. Does not check
    #     the validity of chapter and verse numbers for the book.

    #     """
    #     book, chapter, verse = re.split(r"[: ]", ref, maxsplit=2)
    #     # could be more generous here in matching other abbreviation
    #     # schemes as well
    #     assert book.upper() in BOOKS, f"Invalid book abbreviation: {book}"
    #     usfmbook = BOOKS[book.upper()].usfmnumber
    #     assert int(chapter), f"Chapter must be an integer: {chapter}"
    #     assert int(verse), f"Verse must be an integer: {verse}"
    #     return BCVID(f"{usfmbook}{pad3(chapter)}{pad3(verse)}")

    # @staticmethod
    # def fromlogos(ref) -> "BCVID":
    #     """Return a BCVID instance for a Logos-style single verse reference."""
    #     if ref.startswith("bible") and "." in ref:
    #         bible, restref = ref.split(".", 1)
    #     else:
    #         restref = ref
    #     # eventually we may need to handle different Bible versions
    #     refsplit = restref.split(".")
    #     assert len(refsplit) == 3, f"Invalid reference: {restref}"
    #     # convert e.g. 62 -> "41" (Logos -> USFM), and 1 -> "01"
    #     usfmbook = BOOKS.fromlogos(refsplit[0]).usfmnumber
    #     chapter = pad3(refsplit[1])
    #     verse = pad3(refsplit[2])
    #     return BCVID(f"{usfmbook}{chapter}{verse}")


# really should figure out inheritance here
@dataclass(order=True)
class BCID:
    """Identifies book and chapter from Bible texts.

    This supports BBCCC, where BB identifies a book, and CCC
        identifies a chapter number. Verse is unspecified.

    This dataclass does not validate whether any identifiers are in
    the correct range: it only records the data. Use <TBD> for
    validation. All sequence indices are one-based, not zero-based.

    Attributes:
        book_ID: 2-character string identifying the Bible book using
            USFM numbers (like '40' for Matthew, 'B7' for Enoch)
        chapter_ID: 3-character string identifying a chapter number
            within the book

    See `books.Books.fromusfmnumber()` for how to convert this number
    to other Book identifiers.

    """

    # book mapping data
    ID: str
    book_ID: str = field(init=False)
    chapter_ID: str = field(init=False)
    # the longth of the book+chapter portion of an ID
    _idlen: int = 5

    def __post_init__(self) -> None:
        """Compute other values on initialization."""
        assert len(self.ID) == 5, f"length should be 5 characters: {self.ID}"
        self.book_ID = self.ID[0:2]
        self.chapter_ID = self.ID[2:5]
        # also test that they're all digits, in the right range, etc.

    def __repr__(self) -> str:
        """Return a string representation."""
        return f"{type(self).__name__}('{self.ID}')"

    def includes(self, other: str) -> bool:
        """Return True if other is included in the scope of self.

        Simply based on substring matching. Any instance includes
        itself therefore.

        """
        assert (
            isinstance(other, BCID) or isinstance(other, BCVID) or isinstance(other, BCVWPID)
        ), f"Invalid type with includes(): {other}"
        return other.ID[: self._idlen].startswith(self.ID)

    def to_usfm(self) -> str:
        """Return a USFM representation."""
        usfmbook = BOOKS.fromusfmnumber(self.book_ID).usfmname
        return f"{usfmbook} {int(self.chapter_ID)}"

    # @staticmethod
    # def fromusfm(ref) -> "BCID":
    #     """Return a BCID instance for a USFM-based reference.

    #     Only handles single verse references with a specified chapter
    #     and verse like MRK 4. Does not handle ranges, or non-numeric
    #     verses like 'title'. Does not check the validity of chapter
    #     numbers for the book.

    #     """
    #     book, chapter = re.split(r"[ ]", ref, maxsplit=1)
    #     # could be more generous here in matching other abbreviation
    #     # schemes as well
    #     assert book.upper() in BOOKS, f"Invalid book abbreviation: {book}"
    #     usfmbook = BOOKS[book.upper()].usfmnumber
    #     assert int(chapter), f"Chapter must be an integer: {chapter}"
    #     return BCID(f"{usfmbook}{pad3(chapter)}")

    # @staticmethod
    # def fromlogos(ref) -> "BCID":
    #     """Return a BCVID instance for a Logos-style single chapter reference."""
    #     if ref.startswith("bible") and "." in ref:
    #         bible, restref = ref.split(".", 1)
    #     else:
    #         restref = ref
    #     # eventually we may need to handle different Bible versions
    #     refsplit = restref.split(".")
    #     assert len(refsplit) == 2, f"Invalid reference: {restref}"
    #     # convert e.g. 62 -> "41" (Logos -> USFM), and 1 -> "01"
    #     usfmbook = BOOKS.fromlogos(refsplit[0]).usfmnumber
    #     chapter = pad3(refsplit[1])
    #     return BCID(f"{usfmbook}{chapter}")


@dataclass(order=True, repr=False)
class BCVWPID(BCVID):
    """Identifies words from Bible texts by book, chapter, verse, word, and word part.

    This supports two formats: BBCCCVVVWWW and BBCCCVVVWWWP, where BB
        identifies a book, CCC identifies a chapter number, VVV
        identifies a verse number, and WWW identifies a word number
        within that verse. If P is present it identifies a word part:
        this is only used for Hebrew.

    This dataclass does not validate whether any identifiers are in
    the correct range: it only records the data. Use TBD for
    validation. All sequence indices are one-based, not zero-based.

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
    verse_ID: str = field(init=False)
    word_ID: str = field(init=False)
    part_ID: str = ""
    # the longth of the bcvwp ID
    _idlen = 11

    def __post_init__(self) -> None:
        """Compute other values on initialization."""
        # this should probably delegate to the super class
        # super()__post_init__()
        assert 12 >= len(self.ID) >= 11, f"Invalid length: {self.ID}"
        self.book_ID = self.ID[0:2]
        self.chapter_ID = self.ID[2:5]
        self.verse_ID = self.ID[5:8]
        self.word_ID = self.ID[8:11]
        if len(self.ID) == 12:
            self.part_ID = self.ID[11]
            # TODO: add tests, presumably a closed set of values

    def includes(self, other: str) -> bool:
        """Return True if other is included in the scope of self.

        Simply based on substring matching. Any instance includes
        itself therefore.

        """
        assert isinstance(other, BCVWPID), f"Invalid type with includes(): {other}"
        # only vacuous inclusion
        return self.ID == other.ID

    # not sure this is a proper USFM-ification
    def to_usfm(self) -> str:
        """Return a USFM representation."""
        usfmbook = BOOKS.fromusfmnumber(self.book_ID).usfmname
        return f"{usfmbook} {int(self.chapter_ID)}:{int(self.verse_ID)}"

    # @staticmethod
    # def fromusfm(ref) -> "BCVWPID":
    #     """Return a BCVWPID instance for a USFM-based reference.

    #     Only handles single verse references with a specified chapter
    #     and verse like MRK 4:8. Does not handle ranges, book + chapter
    #     references, or non-numeric verses like 'title'. Does not check
    #     the validity of chapter and verse numbers for the book.

    #     """
    #     book, chapter, verse = re.split(r"[: ]", ref, maxsplit=2)
    #     # could be more generous here in matching other abbreviation
    #     # schemes as well
    #     assert book.upper() in BOOKS, f"Invalid book abbreviation: {book}"
    #     usfmbook = BOOKS[book.upper()].usfmnumber
    #     assert int(chapter), f"Chapter must be an integer: {chapter}"
    #     assert int(verse), f"Verse must be an integer: {verse}"
    #     return BCVWPID(f"{usfmbook}{pad3(chapter)}{pad3(verse)}000")

    # @staticmethod
    # def fromlogos(ref) -> "BCVWPID":
    #     """Return a BCVWPID instance for a Logos-style single verse reference."""
    #     if ref.startswith("bible") and "." in ref:
    #         bible, restref = ref.split(".", 1)
    #     else:
    #         restref = ref
    #     # eventually we may need to handle different Bible versions
    #     refsplit = restref.split(".")
    #     assert len(refsplit) == 3, f"Invalid reference: {restref}"
    #     # convert e.g. 62 -> "41" (Logos -> USFM), and 1 -> "01"
    #     usfmbook = BOOKS.fromlogos(refsplit[0]).usfmnumber
    #     chapter = pad3(refsplit[1])
    #     verse = pad3(refsplit[2])
    #     # append "00" for word
    #     return BCVWPID(f"{usfmbook}{chapter}{verse}000")


# @dataclass
# class MarbleID(BCVWPID:
#     """Like a standard BCVWPID, but with an extra leading digit for books.

#     Format is BBBCCCVVVWWWP."""

#     def __post_init__(self) -> None:
#         """Compute other values on initialization."""
#         # part is not optional
#         assert len(self.ID) == 12, f"Invalid length: {self.ID}"
#         self.book_ID = self.ID[0:2]
#         self.chapter_ID = self.ID[2:5]
#         self.verse_ID = self.ID[5:8]
#         self.word_ID = self.ID[8:11]
#         if len(self.ID) == 12:
#             self.part_ID = self.ID[12]
#             # TODO: add tests, presumably a closed set of values

#     def __repr__(self) -> str:
#         """Return a string representation."""
#         return f"<BCVWPID: {self.ID}>"


reftypes = Union[BID, BCID, BCVID, BCVWPID]


def simplify(refinst, newtype) -> reftypes:
    """Return a 'simpler' new instance for refinst.

    For a BCID, the only simpler form is BID.
    For BCVID, BCID or BID.
    For BCVWID, those or BCVID.
    For BCVWPID, any of the other types.
    """
    assert isinstance(refinst, reftypes), "Must be a reference instance"
    validtypes = {
        "BCID": ["BID"],
        "BCVID": ["BID", "BCID"],
        # no BCVWID yet
        "BCVWPID": ["BID", "BCID", "BCVID"],
    }
    assert refinst.__class__.__name__ in validtypes, f"{newtype} is not a valid simpler type."
    if newtype == "BID":
        return BID(refinst.ID[:2])
    elif newtype == "BCID":
        return BCID(refinst.ID[:5])
    elif newtype == "BCVID":
        return BCVID(refinst.ID[:8])


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
        return f"{arg:0>3}"


#        return "{:03}".format(int(arg))


def fromlogos(ref) -> BID | BCID | BCVID:
    """Return a instance for a Logos-style single verse reference.

    The number of characters determines what kind of instance is returned. At most verse granularity.
    """
    if ref.startswith("bible."):
        bible, baseref = ref.split(".", 1)
    else:
        baseref = ref
    # eventually we may need to handle different Bible versions
    if "." not in baseref:
        # only a book reference
        # bookref = f"{baseref:0>3}"
        return BID(BOOKS.fromlogos(int(baseref)).usfmnumber)
    else:
        # book.rest
        bookref, baseref = baseref.split(".", 1)
        usfmbook = BOOKS.fromlogos(int(bookref)).usfmnumber
        if "." not in baseref:
            # book and chapter
            return BCID(f"{usfmbook}{pad3(baseref)}")
        else:
            # book.chapter.verse
            chapterref, verseref = baseref.split(".", 1)
            # need to test here for no extra cruft?
            return BCVID(f"{usfmbook}{pad3(chapterref)}{pad3(verseref)}")


def fromosis(ref) -> BID | BCID | BCVID:
    """Return a BCV instance for a OSIS-based name reference.

    Only handles book, book + chapter, and book chapter verse
    references like MRK 4:8. Does not handle ranges or non-numeric
    verses like 'title'. Does not check the validity of chapter and
    verse numbers for the book. Book name must be correctly cased.

    """
    if " " not in ref:
        # book only
        usfmbook = BOOKS.fromosis(ref).usfmnumber
        return BID((usfmbook))
    else:
        bookabbrev, rest = ref.split(" ", 1)
        usfmbook = BOOKS.fromosis(bookabbrev).usfmnumber
        if ":" not in rest:
            # book and chapter
            return BCID(f"{usfmbook}{pad3(rest)}")
        else:
            # book, chapter, verse
            chapter, verse = rest.split(":", 1)
            return BCVID(f"{usfmbook}{pad3(chapter)}{pad3(verse)}")


def fromname(ref) -> BID | BCID | BCVID:
    """Return a BCV instance for a full name reference.

    Only handles book, book + chapter, and book chapter verse
    references like 1 Corinthians 4:8. Does not handle ranges or
    non-numeric verses like 'title'. Does not check the validity of
    chapter and verse numbers for the book. Book name must be
    correctly cased and match the `name` column in book/books.tsv.

    """
    # complex check because book names can contain spaces and other numbers
    # must match a regexp of all the book names, and be the same length
    namematch = BOOKS.nameregexp.match(ref)
    assert namematch, f"Invalid name reference: {ref}"
    if len(ref) == (namematch.end() - namematch.start()):
        # book only
        usfmbook = BOOKS.fromname(ref).usfmnumber
        return BID((usfmbook))
    else:
        # split namematch at the end of the match
        bookname, rest = ref[: namematch.end()], ref[(namematch.end() + 1) :]
        usfmbook = BOOKS.fromname(bookname).usfmnumber
        if ":" not in rest:
            # book and chapter
            return BCID(f"{usfmbook}{pad3(rest)}")
        else:
            # book, chapter, verse
            try:
                chapter, verse = rest.split(":", 1)
                return BCVID(f"{usfmbook}{pad3(chapter)}{pad3(verse)}")
            except Exception as e:
                raise ValueError(f"Invalid BCV values: {ref}\n{e}")


def fromusfm(ref) -> BID | BCID | BCVID:
    """Return a BCV instance for a USFM-based reference.

    Only handles book, book + chapter, and book chapter verse
    references like MRK 4:8. Does not handle ranges or non-numeric
    verses like 'title'. Does not check the validity of chapter and
    verse numbers for the book.

    """
    if " " not in ref:
        # book only
        usfmbook = BOOKS[ref.upper()].usfmnumber
        return BID((usfmbook))
    else:
        bookabbrev, rest = ref.split(" ", 1)
        usfmbook = BOOKS[bookabbrev.upper()].usfmnumber
        if ":" not in rest:
            # book and chapter
            return BCID(f"{usfmbook}{pad3(rest)}")
        else:
            # book, chapter, verse
            chapter, verse = rest.split(":", 1)
            return BCVID(f"{usfmbook}{pad3(chapter)}{pad3(verse)}")
