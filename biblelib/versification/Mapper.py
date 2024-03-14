"""Create a mapping from one versification scheme to another.


>>> from biblelib.versification import Mapper

Note some quirks of the versification approach:

- Some Psalms (like PS 23) combine the superscription text (`eng`
verse 0) with verse 1, so `org` verse 1 has more word content than
`eng` does.

"""

import requests
from typing import Any


class Mapper:
    """Create mappings from one versification scheme to another.

    This uses the standard-mappings data from the Copenhagen Alliance.

    Coverage is currently limited to `eng`, `org`, and `rso`
    versifications, and is not guaranteed for books outside the
    Protestant canon.

    """

    jsonbase: str = (
        "https://raw.githubusercontent.com/Copenhagen-Alliance/versification-specification/master/versification-mappings/standard-mappings/"
    )

    def __init__(self, fromscheme: str, toscheme: str) -> None:
        """Create mappings from one versification scheme to another."""
        self.fromscheme = fromscheme
        self.toscheme = toscheme
        self.fromjson = self._load_scheme(self.fromscheme)

    def _load_scheme(self, scheme: str) -> dict[str, Any]:
        """Load json data for scheme."""
        mappingfile = f"{self.jsonbase}/{scheme}.json"
        r = requests.get(mappingfile)
        assert r.status_code == 200, f"Failed to get content from {mappingfile}"
        schemejson: dict[str, Any] = r.json()
        return schemejson
