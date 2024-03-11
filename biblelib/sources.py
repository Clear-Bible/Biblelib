"""Information about source Bible texts."""

from dataclasses import dataclass
from enum import Enum

CANONIDS = {
    "nt",
    "ot",
    # meaning the entire 66 book corpus
    "protestant",
}


class SourceLangEnum(str, Enum):
    """Enumerate lang code values for biblical source languages."""

    aramaic = "arc"
    greek = "grc"
    hebrew = "hbo"


class SourceidEnum(str, Enum):
    """Valid source identifiers."""

    BGNT = "BGNT"
    NA27 = "NA27"
    NA28 = "NA28"
    SBLGNT = "SBLGNT"
    WLC = "WLC"
    WLCM = "WLCM"

    @property
    def canon(self) -> str:
        """Return 'ot' or 'nt' for the canon."""
        if self.value in ["WLC", "WLCM"]:
            return "ot"
        elif self.value in ["BGNT", "NA27", "NA28", "SBLGNT"]:
            return "nt"
        else:
            raise ValueError(f"Unknown error in SourceidEnum.canon for {self.value}")

    # need to add DC, probably others down the road
    @staticmethod
    def get_canon(sourceid: str) -> str:
        """Return a canon string for recognized sources, else 'X'."""
        try:
            srcenum = SourceidEnum(sourceid)
            return srcenum.canon
        except ValueError:
            # unrecognized source
            return "X"
    @staticmethod
    def get_language(sourceid: str) -> str:
        """Return a language string for recognized sources, else 'X'."""
        try:
            srcenum = SourceidEnum(sourceid)
            if srcenum.value in ["WLC", "WLCM"]:
                return "hbo"
            elif srcenum.value in ["BGNT", "NA27", "NA28", "SBLGNT"]:
                return "grc"
        except ValueError:
            raise ValueError(f"Invalid sourceid: {sourceid}")

@dataclass
class Edition:
    """Information about a particular edition of a source text."""
    sourceid: str
    canon: str
    language: str

    @staticmethod
    def from_sourceid(sourceid: str) -> "Edition":
        """Return an Edition object from a sourceid."""
        canon = SourceidEnum.get_canon(sourceid)
        lang = SourceidEnum.get_language(sourceid)
        return Edition(sourceid, canon, lang)
