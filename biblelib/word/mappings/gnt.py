"""Provide word-level mappings between various GNT editions.



Examples:
>>> from biblelib.words.mappings import gnt
>>> gntmap = gnt.GNTMappings()
>>> len(m)
138751
# get the SBLGNT identifier for a MARBLE ref
>>> gntmap.marble2sblgnt("04100604500034")
'n41006045017'

# Note there isn't always a mapping, since the underlying texts vary
# in small ways. So no SBLGNT word corresponding to this UBS word.
>>> gntmap.marble2sblgnt("04000401600012")
''





# to add:
# - show mapping from one text form to another

"""

from collections import UserList
from csv import DictReader
from dataclasses import dataclass
from io import StringIO
import requests
from unicodedata import normalize
from warnings import warn


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

    gitmappings = "https://raw.githubusercontent.com/Clear-Bible/macula-greek/main/sources/Clear/mappings/mappings-GNT-stripped.tsv"

    def __init__(self, sourcefile: str = "") -> None:
        """Initialize GNTMappings."""
        super().__init__()
        r = requests.get(self.gitmappings)
        assert r.status_code == 200, f"Failed to get content from {self.gitmappings}"
        # read the stream into a list of GNTMapping instances
        tablestr = StringIO(r.text)
        reader: DictReader = DictReader(tablestr, dialect="excel-tab")
        # for row in reader:
        #     self.data: list = [GNTMapping(**r) for r in reader]
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
