"""Enumerate the verses for a given versification scheme.

This is utility code for generating VREF files: those who only want to
read those files can ignore this.

The valid schemes are defined by SCHEME_URLS. This draws on the
notebook examples at
https://github.com/Copenhagen-Alliance/versification-specification/versification-mappings/VersificationMappings.ipynb.

No mapping support here yet.

"""

import json
import operator
from pathlib import Path

# This directory: where the bundled scheme JSON files live.
VERSIFICATIONPATH = Path(__file__).parent


# Pinned Copenhagen Alliance commit the bundled scheme JSON was taken from.
# To refresh: run tools/refresh_versification.py (add --latest to repin to
# Copenhagen master HEAD), review the diff, run the tests, and commit.
COPENHAGEN_SHA = "5f3f82f3dc3cfd25fffc6ff04f3630763972258c"
SCHEME_BASE = (
    "https://raw.githubusercontent.com/Copenhagen-Alliance/versification-specification/"
    f"{COPENHAGEN_SHA}/versification-mappings/standard-mappings"
)
# The scheme JSON files ship with the package; these pinned URLs are retained
# for provenance and used by the data-refresh tooling. Only the schemes in
# biblelib.VERSIFICATIONIDS (eng/org/rso) are bundled and supported; add a JSON
# file + entry here to support another. (The former "ethiopian_custom" scheme
# was dropped: its upstream source no longer exists.)
SCHEME_URLS = {scheme: f"{SCHEME_BASE}/{scheme}.json" for scheme in ("eng", "org", "rso")}


class Enumerator:
    """Enumerate the verses for a given versification scheme.

    The valid schemes are defined by SCHEME_URLS.
    """

    def __init__(self, scheme: str) -> None:
        """Instantiate an Enumerator."""
        assert scheme in SCHEME_URLS, f"Invalid scheme: {scheme}"
        self.scheme = scheme
        # the URL is retained for provenance; the data is read from the bundled file
        self.mappingfile = SCHEME_URLS[self.scheme]
        # set this if books is limited to NT or OT
        self.scope: str = ""
        with (VERSIFICATIONPATH / f"{scheme}.json").open(encoding="utf-8") as f:
            self.versedict = json.load(f)

    def books(
        self,
        with_deuterocanon: bool = True,
        nt_only: bool = False,
        ot_only: bool = False,
    ) -> list[str]:
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
        return [
            f"{book} {chapter}:{verse}"
            for verse in range(1, self.chapter_verses(book, chapter) + 1)
        ]

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
