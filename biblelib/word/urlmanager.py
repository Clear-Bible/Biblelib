"""Managing generating URLs for references."""

from typing import Any
from urllib.parse import SplitResult, urlunsplit

from .bcvwpid import BID, BCID, BCVID, BCVIDRange


class URLManager:
    """Manage URLs that point to Bible text."""

    # map web sites offering Bible text to their base URLs
    editions: dict[str, dict[str, Any]] = {
        "bible.com": {
            "ESV": 59,
            "NIRV": 110,
            "NIV": 111,
            "NLT": 116,
            "NASB202": 2692,
            "BSB": 3034,
            # there are many more: add if you wish
        }
    }

    # the authority providing the Bible text
    netloc: str = ""
    # identifies the Bible edition
    edition: str = ""

    def __init__(self, netloc: str = "bible.com", edition: str = "NIV") -> None:
        """Initialize an instance."""
        assert netloc in self.editions, f"Unrecognized netloc {netloc!r} must be a key in editions."
        self.netloc = netloc
        self.edition = edition

    def get_uri(self, bcvref: BCID | BCVID | BCVIDRange, netloc: str = "", edition: str = "") -> str:
        """Return a URI for the given base, edition, and reference."""
        if not netloc:
            netloc = self.netloc
        if edition:
            assert edition in self.editions[netloc], f"Invalid edition {edition}"
        else:
            edition = self.edition
        if isinstance(bcvref, BCVID):
            bookabbrev = BID(bcvref.book_ID).to_usfm()
            refpath = f"{bookabbrev}.{int(bcvref.chapter_ID)}.{int(bcvref.verse_ID)}"
        elif bcvref.__class__.__name__ == "BCID":
            bookabbrev = BID(bcvref.book_ID).to_usfm()
            refpath = f"{bookabbrev}.{int(bcvref.chapter_ID)}"
        elif bcvref.__class__.__name__ == "BID":
            raise NotImplementedError("Can't handle book references")
        elif bcvref.__class__.__name__ == "BCVIDRange":
            if bcvref.cross_chapter:
                raise NotImplementedError("Can't handle cross-chapter references")
            else:
                bookabbrev = BID(bcvref.startid.book_ID).to_usfm()
                refpath = f"{bookabbrev}.{int(bcvref.startid.chapter_ID)}.{int(bcvref.startid.verse_ID)}"
                refpath += f"-{int(bcvref.endid.verse_ID)}"
        #
        if netloc == "bible.com":
            editioncode = self.editions[netloc][edition]
            splitres = SplitResult(
                scheme="https",
                netloc=netloc,
                path=f"/bible/{editioncode}/{refpath}",
                query="",
                fragment="",
            )
        else:
            raise NotImplementedError(f"Can't general URI from {netloc}")
        return urlunsplit(splitres)
