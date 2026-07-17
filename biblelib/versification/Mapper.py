"""Create a mapping from one versification scheme to another.


>>> from biblelib.versification import Mapper

Note some quirks of the versification approach:

- Some Psalms (like PS 23) combine the superscription text (`eng`
verse 0) with verse 1, so `org` verse 1 has more word content than
`eng` does.

"""

import json
from pathlib import Path
from typing import Any

from biblelib import VERSIFICATIONIDS

# This directory: where the bundled scheme JSON files live.
VERSIFICATIONPATH = Path(__file__).parent


class Mapper:
    """Create mappings from one versification scheme to another.

    This uses the standard-mappings data from the Copenhagen Alliance,
    which ships with the package: no network connection is required.

    Coverage is currently limited to `eng`, `org`, and `rso`
    versifications, and is not guaranteed for books outside the
    Protestant canon.

    """

    # Retained for provenance only: the upstream source of the bundled JSON.
    jsonbase: str = "https://raw.githubusercontent.com/Copenhagen-Alliance/versification-specification/master/versification-mappings/standard-mappings/"

    def __init__(self, fromscheme: str, toscheme: str) -> None:
        """Create mappings from one versification scheme to another."""
        assert fromscheme in VERSIFICATIONIDS, f"Unsupported fromscheme: {fromscheme}"
        assert toscheme in VERSIFICATIONIDS, f"Unsupported toscheme: {toscheme}"
        self.fromscheme = fromscheme
        self.toscheme = toscheme
        self.fromjson: dict[str, dict[str, str]] = self._load_scheme(self.fromscheme)

    def _load_scheme(self, scheme: str) -> dict[str, Any]:
        """Load bundled json data for scheme."""
        assert scheme in VERSIFICATIONIDS, f"Unsupported scheme: {scheme}"
        mappingpath = VERSIFICATIONPATH / f"{scheme}.json"
        with mappingpath.open(encoding="utf-8") as f:
            schemejson: dict[str, Any] = json.load(f)
        return schemejson

    # # WORKING HERE
    # def enumerate_mapping(self, fromjson: dict[str, dict[str, str]]) -> list[tuple[str, str]]:
    #     """Return the corresponding reference in the target scheme."""
    #     mappings: list[tuple[str, str]] = []
    #     for fromref, toref in fromjson["mappedVerses"]:
    #         if "-" in fromref:
    #             pass
    #         else:
    #             mappings.append(
    #                 fromusfm(fromref),
    #                 fromusfm(toref),
    #             )
    #         mappings.append((ref, fromjson["mappedVerses"][ref]))
    #     return mappings
