"""This package provides utilities for working with Bible book metadata and collections.

`books` includes mappings between conventional reference systems, and canon lists.

"""

from .books import Book, Books, ProtestantCanon, CatholicCanon


__all__ = [
    "Book",
    "Books",
    "ProtestantCanon",
    "CatholicCanon",
]
