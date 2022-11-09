"""Biblelib provides utilities for working with Bible books, references, pericopes, and other units.

More documentation here.
"""

from .books import Book, Books, CatholicCanon, ProtestantCanon
from .words import ClearID, Mapping, Mappings

__all__ = [
    # books
    "Book",
    "Books",
    # words
    "ClearID",
    "Mapping",
    "Mappings",
]
