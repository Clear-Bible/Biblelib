"""Provide word-level mappings between various GNT editions.



The mapping table is large and is downloaded on first use and cached
locally (see :mod:`biblelib.data`), rather than bundled in the package.

Examples:

>>> from biblelib.word.mappings import gnt
>>> gntmap = gnt.GNTMappings()
>>> len(gntmap)
138750
>>> gntmap.marble2sblgnt("04100604500034")  # SBLGNT id for a MARBLE ref
'n41006045017'

>>> gntmap.marble2sblgnt("04000401600012")  # not every word has a mapping
''





# to add:
# - show mapping from one text form to another

"""

from collections import UserList
from csv import DictReader
from dataclasses import dataclass
from pathlib import Path
from unicodedata import normalize
from warnings import warn

from biblelib import data


@dataclass
class GNTMapping:
    """Dataclass mapping words across various Greek NTs.

    These are read from a TSV file and instantiated by other
    code. Words are identified with the Clear format of an 11-digit
    BBCCCVVVWWW identifier (no canon prefix or word part). Text values
    are UTF-8 encoded, with final punctuation attached.

    Attributes:
        NA1904_ID: the identifier for this word in Nestle-Aland 1904
        NA1904_Text: the word form in Nestle-Aland 1904
        NA27_ID: the identifier in Nestle-Aland 27th Edition
        NA28_ID: the identifier in Nestle-Aland 28th Edition
        SBLGNT_ID: the identifier in SBL GNT
        SBLGNT_Text: the word form in SBL GNT
        MARBLE_ID: the identifier in Project MARBLE

    """

    # Named to match column headers in source TSV
    # Macula ID for the Greek New Testament, edited by Eberhard
    # Nestle: with 'n' corpus prefix
    NA1904_ID: str
    # text element
    NA1904_Text: str
    # Macula ID for Nestle-Aland 27th Edition
    NA27_ID: str
    # Macula ID for Nestle-Aland 28th Edition
    NA28_ID: str
    # Macula ID for https://sblgnt.com/, with 'n' corpus prefix
    SBLGNT_ID: str
    # text element
    SBLGNT_Text: str
    # MARBLE ID for USB project: https://semanticdictionary.org/
    MARBLE_ID: str

    def __post_init__(self) -> None:
        """Compute data after initialization."""
        # add corpus prefixes
        if self.NA1904_ID and not self.NA1904_ID.startswith("n"):
            self.NA1904_ID = f"n{self.NA1904_ID}"
        if self.SBLGNT_ID and not self.SBLGNT_ID.startswith("n"):
            self.SBLGNT_ID = f"n{self.SBLGNT_ID}"
        # ensure both text forms are normalized to aid in testing
        # equality: this means they may differ from original source.
        self.NA1904_Text = normalize("NFC", self.NA1904_Text)
        self.SBLGNT_Text = normalize("NFC", self.SBLGNT_Text)

    def __repr__(self) -> str:
        """Return a string representation."""
        return f"<GNTMapping: {self.SBLGNT_ID}>"

    @property
    def to_marble_id(self) -> str:
        """Return the MARBLE_ID value for self."""
        return self.MARBLE_ID


class GNTMappings(UserList):
    """Manage a sequence of GNTMapping instances."""

    # Retained for provenance only: the upstream source of the mapping data.
    gitmappings = "https://raw.githubusercontent.com/Clear-Bible/macula-greek/main/sources/Clear/mappings/mappings-GNT-stripped.tsv"

    def __init__(self, sourcefile: str = "") -> None:
        """Initialize GNTMappings.

        By default the mapping data is downloaded on first use and read
        from the local cache (see biblelib.data). Pass sourcefile to
        read a different local TSV instead.
        """
        super().__init__()
        path = Path(sourcefile) if sourcefile else data.fetch(data.GNT_MAPPINGS)
        with path.open(encoding="utf-8") as f:
            reader: DictReader = DictReader(f, dialect="excel-tab")
            self.data: list = [GNTMapping(**r) for r in reader]
        # map MARBLE IDs to a GNTMapping instance
        self.marble_ids: dict[str, GNTMapping] = {}
        # map NA28 IDs to a GNTMapping instance
        self.na28_ids: dict[str, GNTMapping] = {}

    def marble2sblgnt(self, marbleid: str) -> str:
        """Return an SBLGNT ID for a MARBLE ID.

        Returns the empty string if the MARBLE ID isn't in the
        mapping, or if there isn't an SBLGNT ID that corresponds.

        """
        # lazy initialization of the dictionary
        if not self.marble_ids:
            for mapping in self.data:
                thismarbleid = mapping.MARBLE_ID
                if thismarbleid:
                    # only store if there's actually an ID
                    if thismarbleid in self.marble_ids:
                        warn(f"Duplicate MARBLE ID {thismarbleid} in {mapping}")
                    self.marble_ids[thismarbleid] = mapping
        mapping = self.marble_ids.get(marbleid)
        mappedstr: str = mapping.SBLGNT_ID if mapping else ""
        return mappedstr

    def na282sblgnt(self, na28id: str) -> str:
        """Return an SBLGNT ID for a NA28 ID.

        Returns the empty string if the NA28 ID isn't in the mapping,
        or if there isn't an SBLGNT ID that corresponds.

        """
        # lazy initialization of the dictionary
        if not self.na28_ids:
            for mapping in self.data:
                thisna28id = mapping.NA28_ID
                if thisna28id:
                    # only store if there's actually an ID
                    if thisna28id in self.na28_ids:
                        warn(f"Duplicate NA28 ID {thisna28id} in {mapping}")
                    self.na28_ids[thisna28id] = mapping
        mapping = self.na28_ids.get(na28id)
        mappedstr: str = mapping.SBLGNT_ID if mapping else ""
        return mappedstr
