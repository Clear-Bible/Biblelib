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

# 'simplify' a reference to contain less granular information
>>> mrk_4_3_1 = BCVWPID("41004003001")
>>> simplify(mrk_4_3_1, BCVID)
BCVID('41004003')
>>> simplify(mrk_4_3_1, BCID)
BCID('41004')
>>> simplify(mrk_4_3_1, BID)
BID('41')



ToDo:
- support Macula-style identifiers: "o"/"n" prefix, no part for Greek
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
import re
from typing import Any, Union, get_args

from biblelib.book import Books


BOOKS = Books()


@dataclass(order=True)
class _Base:
    """Base class for units."""

    # book mapping data
    ID: str
    book_ID: str = field(init=False)
    # the longth of the book portion of an ID
    _idlen: int = 0

    def __post_init__(self) -> None:
        """Compute other values on initialization."""
        assert len(self.ID) == self._idlen, f"length should be {self._idlen} characters: {self.ID}"

    def __repr__(self) -> str:
        """Return a string representation."""
        return f"{type(self).__name__}('{self.ID}')"

    # class is mutable because of post_init, but otherwise logically immutable
    # note that, for subclasses, hash(self) != hash(self.ID). I do not
    # know why, but dataclass hash functions are special.
    def __hash__(self) -> int:
        """Return a hash value."""
        return hash(self.ID)

    @property
    def to_bid(self) -> str:
        """Return the book ID."""
        return self.book_ID


@dataclass(repr=False, unsafe_hash=True)
class BID(_Base):
    """Identifies a book identifier.

    Also a base class for other BCV identifiers.
    """

    # the longth of the book portion of an ID
    _idlen: int = 2

    def __post_init__(self) -> None:
        """Compute other values on initialization."""
        super().__post_init__()
        self.book_ID = self.ID[0:2]
        # also test that they're all digits, in the right range, etc.
        # this covers the protestant canon and deuterocanon, but not perfectly
        # this breaks code in book.py
        # assert re.match("^[0-8][0-9]", self.book_ID), f"Invalid book number {self.book_ID}"

    # could go in a base class?
    # can't reference B*ID types until defined :-/
    def includes(self, other: Any) -> bool:
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
        if isinstance(other, BCVWPID):
            return other.to_bid == self.ID
        else:
            return other.ID[: self._idlen].startswith(self.ID)

    def to_usfm(self) -> str:
        """Return a USFM representation."""
        usfmbook = BOOKS.fromusfmnumber(self.book_ID).usfmname
        return f"{usfmbook}"


@dataclass(repr=False, unsafe_hash=True)
class BCID(BID):
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

    chapter_ID: str = field(init=False)
    # the longth of the book+chapter portion of an ID
    _idlen: int = 5

    def __post_init__(self) -> None:
        """Compute other values on initialization."""
        super().__post_init__()
        self.chapter_ID = self.ID[2:5]
        # also test that they're all digits, in the right range, etc.

    @property
    def to_bcid(self) -> str:
        """Return string for the book and chapter ID."""
        return self.book_ID + self.chapter_ID

    def includes(self, other: Any) -> bool:
        """Return True if other is included in the scope of self.

        Simply based on substring matching. Any instance includes
        itself therefore.

        """
        assert (
            isinstance(other, BCID) or isinstance(other, BCVID) or isinstance(other, BCVWPID)
        ), f"Invalid type with includes(): {other}"
        if isinstance(other, BCVWPID):
            return other.to_bcid == self.ID
        else:
            return other.ID[: self._idlen].startswith(self.ID)

    def to_usfm(self) -> str:
        """Return a USFM representation."""
        usfmbook = BOOKS.fromusfmnumber(self.book_ID).usfmname
        return f"{usfmbook} {int(self.chapter_ID)}"


# ToDo/Idea: should BCVID("41004003001") drop the end of the ID
# string? Same question for BID and BCID, though it seems less common
# that you'd want to upscale those this way.
# Currently it complains the ID arg is too longer: correct, though
# persnickity.


@dataclass(repr=False, unsafe_hash=True)
class BCVID(BCID):
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

    verse_ID: str = field(init=False)
    # the longth of the book+chapter+verse portion of an ID
    _idlen: int = 8

    def __post_init__(self) -> None:
        """Compute other values on initialization."""
        super().__post_init__()
        self.verse_ID = self.ID[5:8]
        # also test that they're all digits, in the right range, etc.

    @property
    def to_bcvid(self) -> str:
        """Return string for the book, chapter, and verse ID."""
        return self.book_ID + self.chapter_ID + self.verse_ID

    def get_id(self) -> str:
        """Return BCVID string. For compatibility with BCVWPID."""
        return self.to_bcvid

    def includes(self, other: Any) -> bool:
        """Return True if other is included in the scope of self.

        Simply based on substring matching. Any instance includes
        itself therefore.

        """
        assert (
            isinstance(other, BCVID)
            # or isinstance(other, BCVWID)
            or isinstance(other, BCVWPID)
        ), f"Invalid type with includes(): {other}"
        if isinstance(other, BCVWPID):
            return other.to_bcvid == self.ID
        else:
            return other.ID[: self._idlen].startswith(self.ID)

    # TODO: add a method to 'upgrade' to BCVWPID given a word_index
    # def _to_bcvwpid(self, word_index: int, part_index: str = "1") -> bcvwpid.BCVWPID:
    #     """Given a BCVID instance and a word index, return a BCVWPID.

    #     Word index should be zero-based.

    #     """
    #     word_ID = pad3(str(word_index + 1))
    #     newidstr = self.ID + word_ID + part_index
    #     return BCVWPID(newidstr)

    def to_usfm(self) -> str:
        """Return a USFM representation."""
        usfmbook = BOOKS.fromusfmnumber(self.book_ID).usfmname
        return f"{usfmbook} {int(self.chapter_ID)}:{int(self.verse_ID)}"


def from_bcid_verse(bcid: BCID, verse: int) -> BCVID:
    """Return a BCVID instance from a BCID and verse number."""
    return BCVID(f"{bcid.ID}{pad3(str(verse))}")


@dataclass
class BCVIDRange:
    """Represents a range of BCVID instances.

    This can represent a range across chapter boundaries,
    though such ranges cannot yet be enumerated.

    It is an error if the start and end books are not the same.
    """

    startid: BCVID
    endid: BCVID
    # these are computed from startid and endid
    ID: str = field(init=False)
    book: BID = field(init=False)
    # initialized from startid, so could be misleading for
    # cross-chapter ranges
    chapter: BCID = field(init=False)
    end_chapter: BCID = field(init=False)

    def __post_init__(self) -> None:
        """Check initialization values."""
        # enforce typs: a little hacky to change init values like this.
        # It would be less hacky to have a factory method that does this.
        if self.startid.__class__.__name__ != "BCVID":
            self.startid = BCVID(self.startid.to_bcvid)
        if self.endid.__class__.__name__ != "BCVID":
            self.endid = BCVID(self.endid.to_bcvid)
        self.ID = self.startid.ID + "-" + self.endid.ID
        self.book: BID = BID(self.startid.to_bid)
        self.chapter: BCID = BCID(self.startid.to_bcid)
        self.end_chapter: BCID = BCID(self.endid.to_bcid)
        assert self.book == BID(
            self.endid.to_bid
        ), f"Startid {self.startid} and endid {self.endid} must be in the same book."
        # note this allows a vacuous range with the same start and
        # end: does that make sense?
        assert self.startid <= self.endid, f"Startid {self.startid} must precede endid {self.endid}."

    def __repr__(self) -> str:
        """Return a printed representation."""
        return f"{type(self).__name__}('{self.ID}')"

    def enumerate(self) -> list[BCVID]:
        """Return a list of BCVID instances enumerating the verses in the range.

        Enumerations include the ending BCVID value (unlike range).

        Only implemented for ranges within the same chapter.  This
        also assumes verse numbers are sequential, without gaps: that
        won't be true for some Bible editions.

        """
        if self.startid == self.endid:
            # vacuous range
            return [self.startid]
        elif self.chapter != self.end_chapter:
            # this needs knowledge about how many Verses in a Chapter,
            # which lives in unit.unitrange. Not sure how to integrate these two:
            # maybe a special enumerate method for cross-chapter ranges?
            raise NotImplementedError("Enumerating over chapter boundaries is not yet implemented.")
        else:
            return [
                from_bcid_verse(self.chapter, n)
                for n in range(int(self.startid.verse_ID), int(self.endid.verse_ID) + 1)
            ]


@dataclass(repr=False, unsafe_hash=True)
class BCVWPID(BCVID):
    """Identifies words from Bible texts by book, chapter, verse, word, and word part.

    The core schema is BBCCCVVVWWWP, where
    - BB identifies a book
    - CCC identifies a chapter number
    - VVV identifies a verse number
    - WWW identifies a word number
    - P optionally identifies a word part: this is optional for NT
      books, where it defaults to 1 if output.

    Identifiers may have an optional canon prefix ("o" or "n"). This
    is removed from the ID but retained as self.canon_prefix.

    This dataclass does not validate whether any identifiers are in
    the correct range: it only records the data. Validation is planned
    for a future version.

    All sequence indices are one-based, not zero-based, and derived
    from the tokenization of the input text (which should be specified
    in its metadata).

    Attributes:
    - canon_prefix: 1-character string identifying the canon, , 'o'
      for OT and 'n' for NT
    - book_ID: 2-character string identifying the Bible book using
      USFM numbers (like '40' for Matthew, 'B7' for Enoch)
    - chapter_ID: 3-character string identifying a chapter number
      within the book
    - verse_ID: 3-character string identifying the verse number
    - word_ID: 3-character string identifying the word number
    - part_ID: single character identifying the word part if present:
      only used for Hebrew

    See `books.Books.fromusfmnumber()` for how to convert this number
    to other Book identifiers.

    """

    # book mapping data
    word_ID: str = field(init=False)
    part_ID: str = ""
    # this is not part of the overall ID, and is computed based on
    # book
    canon_prefix: str = ""
    # the longth of the bcvwp ID
    _idlen = 11

    def __post_init__(self) -> None:
        """Compute other values on initialization.

        This ensures the ID attribute reflects the standardized
        identifier, even if abbreviated forms are initially provided,
        so ID comparison is well-defined.

        """

        def _get_canon_prefix(book_ID: str) -> str:
            """Return a single character prefix for canon."""
            if book_ID < "40":
                return "o"
            elif book_ID < "67":
                return "n"
            else:
                # not sure what's required here
                return "x"

        # cannot call super because allows either 11 or 12 length
        # super()__post_init__()
        assert is_bcvwpid(self.ID), f"Invalid identifier: {self.ID}"
        # assert 13 >= len(self.ID) >= 11, f"Invalid length: {self.ID}"
        if self.ID.startswith("o") or self.ID.startswith("n"):
            self.canon_prefix = self.ID[0]
            restid = self.ID = self.ID[1:]
        else:
            restid = self.ID
            # set canon_prefix and prepend to ID
            self.canon_prefix = _get_canon_prefix(restid[0:2])
            # don't include canon prefix in the ID: decide that at
            # output time with get_id().
            # self.ID = self.canon_prefix + self.ID
        self.book_ID = restid[0:2]
        # TODO: add tests, presumably a closed set of values
        assert self.canon_prefix == _get_canon_prefix(self.book_ID), f"Canon prefix must match book ID: {self.ID}"
        self.chapter_ID = restid[2:5]
        self.verse_ID = restid[5:8]
        self.word_ID = restid[8:11]
        if len(restid) == 12:
            self.part_ID = restid[11]
        else:
            self.part_ID = "1"
            self.ID += self.part_ID

    def get_id(self, prefix: bool = False, part_index: bool = True) -> str:
        """Return a string identifier for the instance.

        With prefix (default=False), prefix OT references with 'o' and
        NT references with 'n'. This is only typcal for Macula source
        references.

        With part_index (default=True), include a part ID, making the
        identifier 12 characters. This is typical for Hebrew, but not
        for Greek or target tokens. Raise ValueError if this would
        drop a non-default part ID.

        """
        strid = self.ID
        if prefix:
            # drop the prefix
            strid = f"{self.canon_prefix}{strid}"
        if not part_index:
            if self.part_ID not in {"", "1"}:
                raise ValueError(f"Unsafe to drop non-default part index: {self}")
            strid = strid[:-1]
        return strid

    def includes(self, other: Any) -> bool:
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


def simplify(refinst: reftypes, newclass: reftypes) -> reftypes:
    """Return a 'simpler' new instance for refinst.

    Simpler here means less specified.
    For a BCID, the only simpler form is BID.
    For BCVID, BCID or BID.
    For BCVWID, BCID, BID, or BCVID.
    For BCVWPID, any of the other types.
    """
    assert refinst.__class__ in get_args(reftypes), f"{refinst} must be a reference instance"
    validtypes = {
        "BCID": ["BID"],
        "BCVID": ["BID", "BCID"],
        # no BCVWID yet
        "BCVWPID": ["BID", "BCID", "BCVID"],
    }
    assert refinst.__class__.__name__ in validtypes, f"{newclass} is not a valid simpler type."
    if isinstance(refinst, BCVWPID):
        if newclass == BID:
            return BID(refinst.to_bid)
        elif newclass == BCID:
            return BCID(refinst.to_bcid)
        elif newclass == BCVID:
            return BCVID(refinst.to_bcvid)
        else:
            raise ValueError(f"Cannot simplify {refinst} to BCVWPID")
    elif newclass == BID:
        return BID(refinst.ID[:2])
    elif newclass == BCID:
        return BCID(refinst.ID[:5])
    elif newclass == BCVID:
        return BCVID(refinst.ID[:8])
    else:
        raise ValueError(f"Invalid refinst to simplify: {refinst}")


def pad3(arg: str) -> str:
    """Return a zero-padded string for an integer.

    "title" is verse 0, so there's possible confusion with unspecified
    verses vs. titles specified as 000.

    """
    if arg == "title":
        return "000"
    else:
        assert len(arg) <= 3, f"Arg must be 3 chars or less: {arg}"
        # handle arg=0
        try:
            int(arg)
        except Exception as e:
            raise ValueError(f"Arg must convert to an int: {arg}\n{e}")
        # return f"{arg:0>3}"
        return arg.zfill(3)


def fromlogos(ref: str) -> BID | BCID | BCVID:
    """Return a instance for a Logos-style single verse reference.

    The number of characters determines what kind of instance is
    returned. At most verse granularity.

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


def fromosis(ref: str) -> BID | BCID | BCVID:
    """Return a BCV instance for a OSIS-based name reference.

    OSIS references use periods for delimiters, like 'Gen.1.1'. Only
    handles book, book + chapter, and book chapter verse references
    like Mark.4.8. Does not handle ranges or non-numeric verses like
    'title'. Does not check the validity of chapter and verse numbers
    for the book. Book name must be correctly cased.

    """
    if "." not in ref:
        # book only
        usfmbook = BOOKS.fromosis(ref).usfmnumber
        return BID((usfmbook))
    else:
        bookabbrev, rest = ref.split(".", 1)
        usfmbook = BOOKS.fromosis(bookabbrev).usfmnumber
        if "." not in rest:
            # book and chapter
            return BCID(f"{usfmbook}{pad3(rest)}")
        else:
            # book, chapter, verse
            chapter, verse = rest.split(".", 1)
            return BCVID(f"{usfmbook}{pad3(chapter)}{pad3(verse)}")


def fromname(ref: str) -> BID | BCID | BCVID:
    """Return a BCV instance for a full name reference.

    Only handles book, book + chapter, and book chapter verse
    references like 1 Corinthians 4:8. Does not handle ranges or
    non-numeric verses like 'title'. Does not check the validity of
    chapter and verse numbers for the book. Book name must be
    correctly cased and match the `name` column in book/books.tsv.

    """
    # complex check because book names can contain spaces and other numbers
    # must match a regexp of all the book names, and be the same length
    # type complaint here: 'str' has no attribute 'match'. Not quite right.
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


def fromusfm(ref: str) -> BID | BCID | BCVID:
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


def frombiblia(ref: str) -> BID | BCID | BCVID:
    """Return a BCV instance for a Biblia-style name reference.

    Only handles book, book + chapter, and book chapter verse
    references like 1Co 4:8. Does not handle ranges or
    non-numeric verses like 'title'. Does not check the validity of
    chapter and verse numbers for the book. Book name must be
    correctly cased and match the `biblia` column in book/books.tsv.

    """
    if " " not in ref:
        # book only
        bibliabook = BOOKS.frombiblia(ref).usfmnumber
        return BID(bibliabook)
    else:
        bookabbrev, rest = ref.split(" ", 1)
        bibliabook = BOOKS.frombiblia(bookabbrev).usfmnumber
        if ":" not in rest:
            # book and chapter
            return BCID(f"{bibliabook}{pad3(rest)}")
        else:
            # book, chapter, verse
            chapter, verse = rest.split(":", 1)
            return BCVID(f"{bibliabook}{pad3(chapter)}{pad3(verse)}")


def to_bcv(token: str | BCVWPID | BCVID) -> str:
    """Return the BCV string for a reference instance or identifier.

    This handles several input types for generality.
    """
    if isinstance(token, BCVWPID):
        return token.to_bcvid
    elif isinstance(token, BCVID):
        return token.ID
    elif isinstance(token, str):
        # convert to a BCVWPID to ensure it's valid (11-12 chars)
        return BCVWPID(token).to_bcvid
    else:
        raise ValueError(f"Invalid token type: {token}")


def make_id(refstr: str) -> BID | BCID | BCVID | BCVWPID:
    """Return an instance of the appropriate class from a ID string.

    Class is chosen based on the length of refstr. Raises a ValueError
    if the length doesn't match expectations.

    """
    idlengths = {
        2: BID,
        5: BCID,
        8: BCVID,
        11: BCVWPID,
        12: BCVWPID,
        13: BCVWPID,
    }
    refclass = idlengths.get(len(refstr))
    if not refclass:
        raise ValueError(f"Can't select appropriate class for {len(refstr)}-character reference {refstr}")
    else:
        instance: BID | BCID | BCVID | BCVWPID = refclass(refstr)
        return instance


def is_bcvwpid(identifier: str) -> bool:
    """Return True if identifier matches the pattern for a BCVWP identifier.

    This does not check validity of book/chapter/verse values, and
    does not enforce e.g. whether target values should have a word
    part: only that it matches the pattern. So it's heuristic at
    best. To really test, use the identifier to create an instance.

    """
    idpat = re.compile(r"^[no]?\d{11,12}$")
    return bool(idpat.match(identifier))
