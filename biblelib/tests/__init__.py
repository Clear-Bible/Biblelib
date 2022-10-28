"""Pytest tests for biblelib.books."""
# import pytest


from biblelib import books


class TestMark(object):
    """Test basic functionality for books."""

    allbooks = books.Books()
    mark = allbooks[40]

    def test_attrs(self):
        """Test attribute values."""
        assert self.mark.usfmnumber == "42"
        assert self.mark.usfmname == "MRK"
        assert self.mark.ososID == "Mark"
