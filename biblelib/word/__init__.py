"""This package provides utilities for working with word-level data from the Hebrew Bible and Greek New Testament.

The Hebrew and Greek source files are available from

*
  [Clear-Bible/macula-hebrew](https://github.com/Clear-Bible/macula-hebrew):
  Syntax trees, morphology, and linguistic annotations for the Hebrew
  Bible

*
  [Clear-Bible/macula-greek](https://github.com/Clear-Bible/macula-greek):
  Syntax trees, morphology, and linguistic annotations for the Greek
  New Testament

"""

from .mappings import Mapping, Mappings
from .bcvwpid import fromlogos, fromname, fromosis, fromusfm, fromubs, reftypes, simplify, BID, BCID, BCVID, BCVWPID

__all__ = [
    # bcvwpid
    "fromlogos",
    "fromname",
    "fromosis",
    "fromusfm",
    "fromubs",
    "reftypes",
    "simplify",
    "BID",
    "BCID",
    "BCVID",
    "BCVWPID",
    # words
    "Mapping",
    "Mappings",
]
