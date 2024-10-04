"""This package provides utilities for working with word-level data from the Hebrew Bible and Greek New Testament.

The Hebrew and Greek source files are available from

* [Clear-Bible/macula-hebrew](https://github.com/Clear-Bible/macula-hebrew):
  Syntax trees, morphology, and linguistic annotations for the Hebrew
  Bible

* [Clear-Bible/macula-greek](https://github.com/Clear-Bible/macula-greek):
  Syntax trees, morphology, and linguistic annotations for the Greek
  New Testament

"""

from biblelib import has_connection

from .bcvwpid import (
    BID,
    BCID,
    BCVID,
    BCVIDRange,
    BCVWPID,
    frombiblia,
    fromlogos,
    fromname,
    fromosis,
    fromusfm,
    reftypes,
    simplify,
    to_bcv,
    make_id,
    is_bcvwpid,
)

# see logic below about when this is really exported
from .ubs import fromubs

_exportlist = [
    # bcvwpid
    "BID",
    "BCID",
    "BCVID",
    "BCVIDRange",
    "BCVWPID",
    "frombiblia",
    "fromlogos",
    "fromname",
    "fromosis",
    "fromusfm",
    "reftypes",
    "simplify",
    "to_bcv",
    "make_id",
    "is_bcvwpid",
]


# this is a bit slow to load: is it worth it?
# you can still load it directly with
# from biblelib.word import ubs
if has_connection():
    _exportlist.append("fromubs")
else:
    print("Cannot load ubs.fromubs(), other functionality is okay.")

__all__ = _exportlist
