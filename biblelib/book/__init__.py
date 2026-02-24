"""This package provides utilities for working with Bible book metadata and collections.

`books` includes mappings between conventional reference systems, and canon lists.

"""

from .book import Book, Books, LocalizedBooks, NTCanon, ProtestantCanon, CatholicCanon, get_localized_books


__all__ = [
    "Book",
    "Books",
    "LocalizedBooks",
    "NTCanon",
    "ProtestantCanon",
    "CatholicCanon",
    "get_localized_books",
]
