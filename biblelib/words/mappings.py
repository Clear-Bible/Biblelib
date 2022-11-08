"""Read and write word-level mappings.

Source data is in ../sources/Clear/mappings/mappings-GNT-stripped.tsv.

Examples:
    >>> from biblelib import words
    >>> m = words.Mappings()
    >>> len(m)
    138804
    >>>
    # to add:
    # - show mapping from one ID to another
    # - show mapping from one text form to another

"""

from collections import UserList
from csv import DictReader, DictWriter
from dataclasses import asdict, dataclass
from pathlib import Path
from unicodedata import normalize


# This directory: mappings-GNT-stripped.tsv is located relative to
# this in a sibling repository
WORDSPATH = Path(__file__).parent
# Content from https://github.com/Clear-Bible/
CLEARPATH = WORDSPATH.parent.parent.parent


@dataclass
class Mapping:
    """Dataclass mapping words across various Greek NTs.

    These are typically read from a TSV file and instantiated by other
    code. Words are identified with the Clear format of an 11-digit
    BBCCCVVVWWW identifier: see documentation for details. Text values
    are UTF-8 encoded, with final punctuation attached.

    Attributes:
        NA1904_ID: the identifier for this word in Nestle-Aland 1904
        NA1904_Text: the word form in Nestle-Aland 1904
        NA27_ID: the identifier in Nestle-Aland 27th Edition
        NA28_ID: the identifier in Nestle-Aland 28th Edition
        SBLGNT_ID: the identifier in SBL GNT
        SBLGNT_Text: the word form in SBL GNT
        MARBLE_ID: the identifier in Project MARBLE

    """

    # Named to match column headers in source TSV
    # Greek New Testament, edited by Eberhard Nestle
    NA1904_ID: str
    # text element
    NA1904_Text: str
    # Nestle-Aland 27th Edition
    NA27_ID: str
    # Nestle-Aland 28th Edition
    NA28_ID: str
    # https://sblgnt.com/
    SBLGNT_ID: str
    # text element
    SBLGNT_Text: str
    # USB MARBLE project: https://semanticdictionary.org/
    MARBLE_ID: str

    def __post_init__(self) -> None:
        """Compute data after initialization."""
        # ensure both text forms are normalized to aid in testing
        # equality: this means they may differ from original source.
        self.NA1904_Text = normalize("NFC", self.NA1904_Text)
        self.SBLGNT_Text = normalize("NFC", self.SBLGNT_Text)

    def __repr__(self) -> str:
        """Return a string representation."""
        return f"<Mapping: {self.NA1904_ID}>"

    def text_eq(self) -> bool:
        """Return True if the NA1904 text is the same as SBLGNT for this mapping.

        The text forms are NFC-normalized on input, so this should
        only be true for 'real' differences.

        """
        return self.NA1904_Text == self.SBLGNT_Text


class Mappings(UserList):
    """Manage a sequence of Mapping instances."""

    # relative path assuming you have a local copy of the macule-greek repo
    source: Path = CLEARPATH / "macula-greek/sources/Clear/mappings/mappings-GNT-stripped.tsv"
    mappingfields: list = list(Mapping.__dataclass_fields__.keys())

    def __init__(self, sourcefile: str = "") -> None:
        """Initialize Mappings."""
        super().__init__()
        if sourcefile:
            self.source = Path(sourcefile)
        assert self.source.exists(), f"No file {self.source}: do you have a local copy of the macula-greek repository?"
        with self.source.open(encoding="utf-8") as f:
            reader: DictReader = DictReader(f, dialect="excel-tab")
            # make sure the fieldnames in the file are the same as the
            # dataclass attributes
            fieldnameset: set = set(reader.fieldnames[0].split("\t"))
            assert not fieldnameset.difference(
                self.mappingfields
            ), f"Fieldname discrepancy header: {fieldnameset} vs {self.mappingfields}"
            self.data: list = [Mapping(**r) for r in reader]

    # short-term need
    def _add_prefix(
        self, outfile: str = CLEARPATH / "macula-greek/sources/Clear/mappings/mappings-GNT-corrected.tsv"
    ) -> None:
        """Rewrite the source, adding 'n' to NA1904_ID values."""
        outpath = Path(outfile)
        with outpath.open("w", encoding="utf-8") as f:
            writer: DictWriter = DictWriter(f, fieldnames=self.mappingfields, dialect="excel-tab")
            writer.writeheader()
            for mapping in self.data:
                mapping.NA1904_ID = "n" + mapping.NA1904_ID
                writer.writerow(asdict(mapping))
