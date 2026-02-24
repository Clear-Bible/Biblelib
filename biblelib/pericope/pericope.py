"""Manage pericope data for Bible books.

A pericope is a short, conventionalized unit of Bible text. Each verse
in a Bible belongs to exactly one pericope within a given edition's
pericope set. Pericopes are loaded from TSV files named
``pericopes_<lang>_<version>.tsv``.

>>> from biblelib.pericope.pericope import PericopeDict
>>> bsb = PericopeDict(language="eng", version="BSB", license="CC BY 4.0")
>>> len(bsb) > 0
True
>>> bsb[0].title
'The Creation'
>>> bsb[0].startid
BCVID('01001001')
>>> sower = bsb.get_pericope(BCVID("41004003"))
>>> sower
Pericope(index=1679, title='The Parable of the Sower')
>>> sower.startid, sower.endid
BCVID('41004001'), BCVID('41004009')
>>> sower.next()
Pericope(index=1680, title='The Reason for the Parables')
>>> sower.previous()
Pericope(index=1678, title='Jesus’ Mother and Brothers')
>>> sower < sower.next()
True
"""

from __future__ import annotations

import csv
from collections import UserDict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from biblelib.word import BID, BCVID, BCVIDRange

# The directory containing bundled pericope data files.
_PERICOPE_DIR = Path(__file__).parent


@dataclass(eq=False)
class Pericope:
    """An individual unit of a Bible text.

    Pericope instances do not contain actual verse text, only references.
    Other code is needed to retrieve textual content.

    Attributes:
        startid: the BCVID instance for the first verse in the pericope
        endid: the BCVID instance for the last verse in the pericope
        title: a brief localized string providing a title for the pericope
        index: the integer index of this pericope within its parent, zero-based
        parent: the PericopeDict to which this Pericope belongs
        extras: dict of values from additional columns in the source TSV
        book: the BID for the book this pericope belongs to (derived from startid)
    """

    startid: BCVID
    endid: BCVID
    title: str
    index: int
    parent: PericopeDict
    extras: dict[str, str] = field(default_factory=dict)
    book: BID = field(init=False)

    def __post_init__(self) -> None:
        """Compute derived attributes."""
        self.book = BID(self.startid.to_bid)

    def __repr__(self) -> str:
        """Return a string representation."""
        return f"Pericope(index={self.index}, title={self.title!r})"

    def __hash__(self) -> int:
        """Return a hash value based on parent identity and index."""
        return hash((id(self.parent), self.index))

    def __eq__(self, other: object) -> bool:
        """Return True if other has the same parent and index.

        Two Pericope instances are equal if they have the same parent
        PericopeDict and the same index.
        """
        if not isinstance(other, Pericope):
            return NotImplemented
        return self.parent is other.parent and self.index == other.index

    def __lt__(self, other: Pericope) -> bool:
        """Return True if other is a later pericope in the same parent.

        Raises AssertionError if the two pericopes have different parents.
        """
        assert self.parent is other.parent, "Cannot compare pericopes from different PericopeDicts."
        return self.index < other.index

    def __gt__(self, other: Pericope) -> bool:
        """Return True if other is an earlier pericope in the same parent.

        Raises AssertionError if the two pericopes have different parents.
        """
        assert self.parent is other.parent, "Cannot compare pericopes from different PericopeDicts."
        return self.index > other.index

    def __le__(self, other: Pericope) -> bool:
        """Return True if other is the same or a later pericope in the same parent.

        Raises AssertionError if the two pericopes have different parents.
        """
        assert self.parent is other.parent, "Cannot compare pericopes from different PericopeDicts."
        return self.index <= other.index

    def __ge__(self, other: Pericope) -> bool:
        """Return True if other is the same or an earlier pericope in the same parent.

        Raises AssertionError if the two pericopes have different parents.
        """
        assert self.parent is other.parent, "Cannot compare pericopes from different PericopeDicts."
        return self.index >= other.index

    @property
    def language(self) -> str:
        """Return the language of the parent PericopeDict."""
        return self.parent.language

    @property
    def version(self) -> str:
        """Return the version of the parent PericopeDict."""
        return self.parent.version

    def contains(self, bcvid: BCVID) -> bool:
        """Return True if bcvid falls within this pericope's range."""
        return self.startid <= bcvid <= self.endid

    def next(self) -> Optional[Pericope]:
        """Return the next Pericope in the sequence, or None if this is the last."""
        return self.parent.data.get(self.index + 1)

    def previous(self) -> Optional[Pericope]:
        """Return the previous Pericope in the sequence, or None if this is the first."""
        if self.index == 0:
            return None
        return self.parent.data.get(self.index - 1)


class PericopeDict(UserDict):  # type: ignore[type-arg]
    """An ordered collection of Pericope instances from a Bible edition.

    Pericopes are keyed by zero-based integer indices and loaded from a
    TSV file named ``pericopes_<language>_<version>.tsv``.

    Attributes:
        language: an ISO-639 language code
        version: a standardized abbreviation like "NIV2011"
        license: a standard license identifier
        path: the path from which pericope data is loaded
        data: a dictionary pairing zero-based integer indices with Pericope instances
    """

    language: str
    version: str
    license: str
    path: Path

    def __init__(
        self,
        language: str,
        version: str,
        license: str = "",
        path: Optional[Path] = None,
    ) -> None:
        """Initialize and load pericope data from a TSV file.

        Args:
            language: ISO-639 language code (e.g. "eng")
            version: version abbreviation (e.g. "BSB")
            license: license identifier (e.g. "CC BY 4.0")
            path: path to the TSV file; defaults to the bundled file
                for the given language and version
        """
        super().__init__()
        self.language = language
        self.version = version
        self.license = license
        if path is None:
            path = _PERICOPE_DIR / f"pericopes_{language}_{version}.tsv"
        self.path = path
        self._load()

    def __eq__(self, other: object) -> bool:
        """Return True if other has the same language and version."""
        if not isinstance(other, PericopeDict):
            return NotImplemented
        return self.language == other.language and self.version == other.version

    def __hash__(self) -> int:
        """Return a hash value based on language and version."""
        return hash((self.language, self.version))

    def _load(self) -> None:
        """Load pericope data from the TSV file."""
        with open(self.path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for index, row in enumerate(reader):
                startid = BCVID(row["startid"])
                endid = BCVID(row["endid"])
                title = row["title"]
                extras: dict[str, str] = {k: str(v) for k, v in row.items() if k not in ("startid", "endid", "title")}
                pericope = Pericope(
                    startid=startid,
                    endid=endid,
                    title=title,
                    index=index,
                    parent=self,
                    extras=extras,
                )
                self.data[index] = pericope

    def get_pericope(self, bcvid: BCVID) -> Pericope:
        """Return the Pericope that contains this verse.

        Raises:
            ValueError: if bcvid does not occur in any pericope.
        """
        for pericope in self.data.values():
            if pericope.contains(bcvid):
                return pericope
        raise ValueError(f"No pericope found containing {bcvid!r}")

    def get_pericopes(self, bcvidrange: BCVIDRange) -> list[Pericope]:
        """Return the ordered list of pericopes that intersect with this range.

        Raises:
            ValueError: if no pericopes are found for the given range.
        """
        result = [
            pericope
            for pericope in self.data.values()
            if pericope.startid <= bcvidrange.endid and pericope.endid >= bcvidrange.startid
        ]
        if not result:
            raise ValueError(f"No pericopes found for range {bcvidrange!r}")
        return result

    def get_book_pericopes(self, bid: BID) -> list[Pericope]:
        """Return the complete list of pericopes for this book."""
        return [p for p in self.data.values() if p.book == bid]
