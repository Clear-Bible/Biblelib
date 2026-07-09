"""Map MARBLE references to WLCM and SBLGNT references."""

import re
from functools import cache
from warnings import warn

from .gnt import GNTMappings
from .wlcm import WLCMMappings


@cache
def gnt_mappings() -> GNTMappings:
    """Return the shared GNT mappings, loading them on first use.

    The underlying data is downloaded and cached on first access, not
    at import time, so importing this module has no network cost.
    """
    return GNTMappings()


@cache
def wlcm_mappings() -> WLCMMappings:
    """Return the shared WLCM (Hebrew) mappings, loading them on first use."""
    return WLCMMappings()


class Mapper:
    """Map MARBLE references to WLCM and SBLGNT references."""

    @property
    def gnt(self) -> GNTMappings:
        """The GNT mappings (shared, loaded on first use)."""
        return gnt_mappings()

    @property
    def wlcm(self) -> WLCMMappings:
        """The WLCM (Hebrew) mappings (shared, loaded on first use)."""
        return wlcm_mappings()

    def to_macula(self, marbleid: str) -> list[str]:
        """Map a MARBLE reference to a list of WLCM or SBLGNT references.

        This only handles word/part-level references. Use
        bcvwpid.from_ubs() to handle the more general case of BCV
        references.

        """
        # some UBS DGNT references have this as a suffix: fragile
        if re.search(r"\({N:00\d}\)$", marbleid) or re.search(r"{N:00\d}$", marbleid):
            marbleid = marbleid[:14]
        assert len(marbleid) == 14, f"{len(marbleid)} characters, not a UBS reference: {marbleid}"

        bookid = marbleid[:3]
        if "000" < bookid < "040":
            return self.wlcm.marble2macula(marbleid)
        elif "039" < bookid < "067":
            sblgnt = self.gnt.marble2sblgnt(marbleid)
            return [sblgnt] if sblgnt else []
        else:
            warn(f"Invalid book ID for MARBLE ID: {marbleid}")
            return []
