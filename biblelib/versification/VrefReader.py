"""Read standard versification files.


>>> from biblelib.versification import VrefReader
>>> eng_nt = VrefReader("eng", "nt")
>>> len(eng_nt)
7959
>>> eng_nt[1187]  # default: references are converted to BCV
'41004009'
>>> eng_nt = VrefReader("eng", "nt", asbcv=False)  # leave as USFM
>>> eng_nt[1187]
'MRK 4:9'

"""

from collections import UserList
from pathlib import Path

from biblelib import CANONIDS, VERSIFICATIONIDS
from biblelib.word import bcvwpid

# This directory: where the bundled *-vref.txt files live.
VERSIFICATIONPATH = Path(__file__).parent


class VrefReader(UserList):
    """Read a vref file with versification data.

    The vref files ship with the package and are read locally: no
    network connection is required.

    """

    # Retained for provenance only: the upstream source of the bundled vref files.
    #
    # IMPORTANT: do not remove or rename the bundled `*-vref.txt` files. Older
    # Biblelib releases (<= 0.5.4) fetch them from this raw URL at runtime, so
    # deleting them from the repo would 404 that request and break clients that
    # are already deployed. They are kept in sync with the bundled scheme JSON by
    # tests/versification/test_vref_derivation.py.
    remote_vrefbase: str = "https://raw.githubusercontent.com/Clear-Bible/Biblelib/master/biblelib/versification/"

    def __init__(self, scheme: str, canon: str, asbcv: bool = True, sourcefile: str = "") -> None:
        """Read a .vref file.

        With asbcv=True (the default), converts references from USFM
        to BCV: otherwise they remain as USFM.

        The bundled vref file for the scheme and canon is read by
        default; pass sourcefile to read a different local file.

        """
        assert scheme in VERSIFICATIONIDS, f"Unsupported scheme: {scheme}"
        assert canon in CANONIDS, f"Unsupported canon: {canon}"
        self.scheme = scheme
        self.canon = canon
        self.vref_file: Path = Path(sourcefile) if sourcefile else self.get_vref_file(scheme, canon)
        vref_usfm: list[str] = self.vref_file.read_text(encoding="utf-8").split("\n")
        if asbcv:
            # convert to BCV, dropping any trailing blank line
            self.data: list[str] = [bcvwpid.fromusfm(usfm).ID for usfm in vref_usfm if usfm]
        else:
            self.data = [usfm for usfm in vref_usfm if usfm]

    def get_vref_file(self, scheme: str, canon: str) -> Path:
        """Return the path to the bundled VREF file for scheme and canon."""
        return VERSIFICATIONPATH / f"{scheme}-{canon}-vref.txt"
