"""Read standard versification files.


>>> from biblelib.versification import VrefReader
>>> eng_nt = VrefReader("eng", "nt")
>>> len(eng_nt)
7959
# default is convert to BCV references
>>> eng_nt[1187]
"41004009"
# leave as USFM
>>> eng_nt = VrefReader("eng", "nt", asbcv=False)
>>> eng_nt[1187]
"MRK 4:9"

"""

from collections import UserList
import json
import requests
from string import Template
from typing import Any

from biblelib.word import bcvwpid


class VrefReader(UserList):
    """Read a vref file with versification data."""

    schemes: set[str] = {
        "eng",
        "org",
        "rso",
        # not yet implemented
        # "ethiopian_custom", "lxx", "rsc", "vul"
    }
    canons: set[str] = {"nt", "ot", "protestant"}
    vrefbase: str = "https://raw.githubusercontent.com/Clear-Bible/Biblelib/master/biblelib/versification/"

    def __init__(self, scheme: str, canon: str, asbcv: bool = True) -> None:
        """Read a .vref file.

        With asbcv=True (the default), converts references from USFM
        to BCV: otherwise they remain as USFM.

        """
        self.scheme = scheme
        self.canon = canon
        self.vref_file: str = self.get_vref_file(scheme, canon)
        r = requests.get(self.vref_file)
        assert r.status_code == 200, f"Failed to get content from {self.vref_file}"
        vref_usfm: list[str] = r.text.split("\n")
        if asbcv:
            # convert to BCVdrop the last blank string
            self.data: list[str] = [bcvwpid.fromusfm(usfm).ID for usfm in vref_usfm if usfm]
        else:
            self.data = vref_usfm

    def get_vref_file(self, scheme: str, canon: str) -> str:
        """Return the path to a VREF file for scheme and canon."""
        return self.vrefbase + f"{scheme}-{canon}-vref.txt"


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

    def _load_scheme(self, scheme: str) -> dict[str, Any]:
        """Load json data for scheme."""
        mappingfile = f"{self.jsonbase}/{scheme}.json"
        r = requests.get(mappingfile)
        assert r.status_code == 200, f"Failed to get content from {mappingfile}"
        schemejson: dict[str, Any] = r.json()
        return schemejson
