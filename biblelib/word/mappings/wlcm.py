"""Provide word-level mappings between Macula Hebrew (WLCM) and MARBLE.



The mapping table is large and is downloaded on first use and cached
locally (see :mod:`biblelib.data`), rather than bundled in the package.

Examples:

>>> from biblelib.word.mappings import wlcm
>>> wlcmmap = wlcm.WLCMMappings()
>>> len(wlcmmap)
420059
>>> wlcmmap.marble2macula("00100100100016")  # MACULA id(s) for a MARBLE ref
['o010010010061']





# to add:
# - show mapping from one text form to another

"""

from collections import UserList
from csv import DictReader
from dataclasses import dataclass
from pathlib import Path
from warnings import warn

from biblelib import data


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

    # Retained for provenance only: the upstream source of the mapping data.
    gitmappings = "https://raw.githubusercontent.com/Clear-Bible/macula-hebrew/main/mappings/tsv/macula_to_marble_map.tsv"

    def __init__(self, sourcefile: str = "") -> None:
        """Initialize WLCMMappings.

        By default the mapping data is downloaded on first use and read
        from the local cache (see biblelib.data). Pass sourcefile to
        read a different local TSV instead.
        """
        super().__init__()
        path = Path(sourcefile) if sourcefile else data.fetch(data.WLCM_MAPPINGS)
        with path.open(encoding="utf-8") as f:
            reader: DictReader = DictReader(f, dialect="excel-tab")
            self.data: list = [WLCMMapping(**r) for r in reader]
        # map MARBLE IDs to a WLCMMapping instance
        self.marble_ids: dict[str, WLCMMapping] = {}

    def marble2macula(self, marbleid: str) -> list[str]:
        """Return one or more MACULA IDs for a MARBLE ID.

        Returns the empty string if the MARBLE ID isn't in the
        mapping, or if there isn't an MACULA ID that corresponds.

        """
        # check for valid range
        assert (
            "000" < marbleid[:3] < "040"
        ), f"Invalid book range for MARBLE ID: {marbleid}"
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
        mappedstr: list[str] = mapping.MACULA_IDs.split(" ") if mapping else []
        return mappedstr
