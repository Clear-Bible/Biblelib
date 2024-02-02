"""This package defines structural units of Bible text.

There's no word content at present: instead, this is for working with
books, chapters, and verses, their references, and components.

"""

# this can cause circular imports if files _in this module_ import
# from biblelib.unit directly. Instead do e.g.
# `from biblelib.unit.verse import Verse`
# (*not* `from biblelib.unit import Verse`)
from .book import BookChapters
from .chapter import Chapters, Chapter
from .unitrange import ChapterRange, VerseRange
from .unit import Unit, Versification, pad
from .verse import Verse

__all__ = [
    # book
    "BookChapters",
    # chapter
    "Chapters",
    "Chapter",
    # unitrange
    "ChapterRange",
    "VerseRange",
    # unit
    "Unit",
    "Versification",
    "pad",
    # verse
    "Verse",
]
