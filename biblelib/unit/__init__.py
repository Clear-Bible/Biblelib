"""This package defines structural units of Bible text.

There's no word content at present: instead, this is for working with
books, chapters, and verses, their references, and components.

"""

from .chapter import Chapters, Chapter
from .unit import Unit, Versification, pad
from .verse import Verse

__all__ = [
    # book
    "BookChapters",
    # chapter
    "Chapters",
    "Chapter",
    # unit
    "Unit",
    "Versification",
    "pad",
    # verse
    "Verse",
]
