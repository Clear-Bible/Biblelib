"""Map MARBLE references to WLCM and SBLGNT references."""

import re
from warnings import warn

from .gnt import GNTMappings
from .wlcm import WLCMMappings


class Mapper:
    """Map MARBLE references to WLCM and SBLGNT references."""

    gnt = GNTMappings()
    wlcm = WLCMMappings()

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
