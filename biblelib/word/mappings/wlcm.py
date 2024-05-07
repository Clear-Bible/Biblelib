"""Provide word-level mappings between Macula Hebrew (WLCM) and MARBLE.



Examples:
>>> from biblelib.words.mappings import gnt
>>> gntmap = gnt.WLCMMappings()
>>> len(m)
138751
# get the SBLGNT identifier for a MARBLE ref
>>> gntmap.marble2sblgnt("04100604500034")
'41006045017'

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
from warnings import warn


@dataclass
class WLCMMapping:
    """Dataclass mapping words across Macula Hebrew and MARBLE.

    These are read from a TSV file.. Macula tokens are identified with
    the Clear format of an 11-digit BBCCCVVVWWW identifier, with canon
    prefix. MARBLE values have no canon prefix.

    Attributes:
        MACULA_IDs: the identifier in Macula Hebrew
        MARBLE_IDs: the identifier in Project MARBLE

    """

    # Named to match column headers in source TSV
    #
    # Macula ID for WLC(M). Could be two (or more?) IDs separated by a space.
    MACULA_IDs: str
    # MARBLE ID for USB project: https://semanticdictionary.org/
    MARBLE_IDs: str

    def __post_init__(self) -> None:
        """Initialize data."""
        assert self.MACULA_IDs.startswith("o"), f"Invalid Macula id: {self.MACULA_IDs}"

    def __repr__(self) -> str:
        """Return a string representation."""
        return f"<WLCMMapping: {self.MACULA_IDs}>"

    @property
    def to_marble_id(self) -> str:
        """Return the MARBLE_ID value for self."""
        return self.MARBLE_IDs


class WLCMMappings(UserList):
    """Manage a sequence of WLCMMapping instances."""

    gitmappings = (
        "https://raw.githubusercontent.com/Clear-Bible/macula-hebrew/main/mappings/tsv/macula_to_marble_map.tsv"
    )

    def __init__(self, sourcefile: str = "") -> None:
        """Initialize WLCMMappings."""
        super().__init__()
        r = requests.get(self.gitmappings)
        assert r.status_code == 200, f"Failed to get content from {self.gitmappings}"
        # read the stream into a list of WLCMMapping instances
        tablestr = StringIO(r.text)
        reader: DictReader = DictReader(tablestr, dialect="excel-tab")
        # for row in reader:
        #     self.data: list = [WLCMMapping(**r) for r in reader]
        self.data: list = [WLCMMapping(**r) for r in reader]
        # map MARBLE IDs to a WLCMMapping instance
        self.marble_ids: dict[str, WLCMMapping] = {}

    def marble2macula(self, marbleid: str) -> list[str]:
        """Return one or more MACULA IDs for a MARBLE ID.

        Returns the empty string if the MARBLE ID isn't in the
        mapping, or if there isn't an MACULA ID that corresponds.

        """
        # check for valid range
        assert ("000" < marbleid[:3] < "040"), f"Invalid book range for MARBLE ID: {marbleid}"
        # lazy initialization of the dictionary
        if not self.marble_ids:
            for mapping in self.data:
                thismarbleid = mapping.MARBLE_IDs
                if thismarbleid:
                    # only store if there's actually an ID
                    if thismarbleid in self.marble_ids:
                        warn(f"Duplicate MARBLE ID {thismarbleid} in {mapping}")
                    self.marble_ids[thismarbleid] = mapping
        mapping = self.marble_ids.get(marbleid)
        mappedstr: list[str] = mapping.MACULA_IDs.split(" ") if mapping else ""
        return mappedstr
