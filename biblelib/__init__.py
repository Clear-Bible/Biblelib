"""Utilities for working with Bible books, references, pericopes, and other units."""

import os
import pathlib

# from biblelib.books import Book
# from biblelib.groups import BookGroups
# from biblelib.core import fromdtr
# from biblelib.bibledatatypes import (
#     BIBLEDATATYPES,
#     isrecognizedtype,
#     human_datatype,
#     datatype_language,
#     datatype_abbreviation,
# )

# from .pericopes
# from .biblia


__version__ = "0.7.6"
__title__ = "biblelib"
__description__ = "Utilities for working with Bible books, references, pericopes, and other units."
__uri__ = "http://github.com/Clear-Bible/Biblelib"
__doc__ = __description__ + " <" + __uri__ + ">"

__author__ = "Sean Boisen"
__email__ = "sean.boisen@clear.bible"

__license__ = "MIT"
__copyright__ = "Copyright (c) 2018 Faithlife Corporation"


# __all__ = [
#     # books
#     'Book',
#     # core.py
#     'fromdtr',
#     # bibledatatypes.py
#     'BIBLEDATATYPES', 'isrecognizedtype', 'human_datatype',
#     'datatype_language', 'datatype_abbreviation',
#     # groups.py
#     'BookGroups'
# ]


# USERHOMEDIR = pathlib.Path(os.path.expanduser('~'))
# if "REPODIR" in os.environ:
#     REPODIR = pathlib.Path(os.environ['REPODIR'])
# else:
#     # YMMV
#     REPODIR = USERHOMEDIR / "git/CI/LogosPericopeAPI"
# DATADIR = REPODIR / "data"
