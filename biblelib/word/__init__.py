"""This package provides utilities for working with word-level data from the Hebrew Bible and Greek New Testament.

The Hebrew and Greek source files are available from

* [Clear-Bible/macula-hebrew](https://github.com/Clear-Bible/macula-hebrew):
  Syntax trees, morphology, and linguistic annotations for the Hebrew
  Bible

* [Clear-Bible/macula-greek](https://github.com/Clear-Bible/macula-greek):
  Syntax trees, morphology, and linguistic annotations for the Greek
  New Testament

"""

from .mappings import Mapping, Mappings
from .bcvwpid import (
    BID,
    BCID,
    BCVID,
    BCVWPID,
    fromlogos,
    fromname,
    fromosis,
    fromusfm,
    fromubs,
    reftypes,
    simplify,
    to_bcv,
)

__all__ = [
    # bcvwpid
    "BID",
    "BCID",
    "BCVID",
    "BCVWPID",
    "fromlogos",
    "fromname",
    "fromosis",
    "fromusfm",
    "fromubs",
    "reftypes",
    "simplify",
    "to_bcv",
    # words
    "Mapping",
    "Mappings",
]
