"""Enumerate the verses for a given versification scheme.

This is utility code for generating VREF files: those who only want to
read those files can ignore this.

The valid schemes are defined by SCHEME_URLS. This draws on the
notebook examples at
https://github.com/Copenhagen-Alliance/versification-specification/versification-mappings/VersificationMappings.ipynb.

No mapping support here yet.

"""

import operator
from pathlib import Path
import requests
from typing import Any, Mapping

from biblelib import has_connection

if not has_connection():
    print("Cannot load Enumerator without network connection.")


SCHEME_URLS = {
    "eng": "https://raw.githubusercontent.com/Copenhagen-Alliance/versification-specification/master/versification-mappings/standard-mappings/eng.json",
    "org": "https://raw.githubusercontent.com/Copenhagen-Alliance/versification-specification/master/versification-mappings/standard-mappings/org.json",
    "rsc": "https://raw.githubusercontent.com/Copenhagen-Alliance/versification-specification/master/versification-mappings/standard-mappings/rsc.json",
    "rso": "https://raw.githubusercontent.com/Copenhagen-Alliance/versification-specification/master/versification-mappings/standard-mappings/rso.json",
    "lxx": "https://raw.githubusercontent.com/Copenhagen-Alliance/versification-specification/master/versification-mappings/standard-mappings/lxx.json",
    "vul": "https://raw.githubusercontent.com/Copenhagen-Alliance/versification-specification/master/versification-mappings/standard-mappings/vul.json",
    "ethiopian_custom": "https://raw.githubusercontent.com/Copenhagen-Alliance/versification-specification/master/versification-mappings/custom-mappings/ethiopian.json",
}


class Enumerator:
    """Enumerate the verses for a given versification scheme.

    The valid schemes are defined by SCHEME_URLS.
    """

    def __init__(self, scheme: str) -> None:
        """Instantiate an Enumerator."""
        assert scheme in SCHEME_URLS, f"Invalid scheme: {scheme}"
        self.scheme = scheme
        self.mappingfile = SCHEME_URLS[self.scheme]
        # set this if books is limited to NT or OT
        self.scope: str = ""
        r = requests.get(self.mappingfile)
        assert r.status_code == 200, f"Failed to get content from {self.mappingfile}"
        self.versedict = r.json()

    def books(self, with_deuterocanon: bool = True, nt_only: bool = False, ot_only: bool = False) -> list[str]:
        """Return a list of USFM book names in this versification.

        With nt_only, only return books in the NT, excluding the
        deuterocanon. Likewise with ot_only. Otherwise, return all
        books, unless with_deuterocanon is False, in which case only
        return books in the Protestant canon.  Some of these options
        may be mutually exclusive.

        """
        booknames: list[str] = list(self.versedict["maxVerses"].keys())
        if nt_only:
            assert not ot_only, "nt_only and ot_only are mutually exclusive"
            self.scope = "nt"
            matindex = operator.indexOf(booknames, "MAT")
            revindex = operator.indexOf(booknames, "REV")
            return booknames[matindex : (revindex + 1)]
        elif ot_only:
            assert not nt_only, "nt_only and ot_only are mutually exclusive"
            self.scope = "ot"
            malindex = operator.indexOf(booknames, "MAL")
            return booknames[: malindex + 1]
        elif not with_deuterocanon:
            self.scope = "protestant"
            # this assumes DC books always start after Rev: is that
            # true beyond org?
            revindex = operator.indexOf(self.books(), "REV")
            return booknames[: (revindex + 1)]
        else:
            return booknames

    def chapter_verses(self, book: str, chapter: int) -> int:
        """Return the number of verses in a given chapter.

        The chapter index is the traditional 1-based value.
        """
        return int(self.versedict["maxVerses"][book][chapter - 1])

    def enumerate_verses(self, book: str, chapter: int) -> list[str]:
        """Return a list of USFM references for a given book and chapter."""
        return [f"{book} {chapter}:{verse}" for verse in range(1, self.chapter_verses(book, chapter) + 1)]

    def write_enumeration(self, outpath: Path, *args: bool, **kwargs: bool) -> None:
        """Write the enumeration to a txt file."""
        booknames: list[str] = self.books(*args, **kwargs)
        if not outpath:
            thisdir = Path(__file__).parent
            if self.scope:
                fileid = f"{self.scheme}-{self.scope}"
            else:
                fileid = f"{self.scheme}"
            outpath = thisdir / f"{fileid}-vref.txt"
        with outpath.open("w") as f:
            for book in booknames:
                # assumes chapters start at 1: not LetJer
                maxchapters: int = len(self.versedict["maxVerses"][book]) + 1
                for chapterindex in range(1, maxchapters):
                    for verse in self.enumerate_verses(book, chapterindex):
                        f.write(f"{verse}\n")
