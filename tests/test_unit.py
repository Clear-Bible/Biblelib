"""Pytest tests for biblelib.unit."""
# import pytest


from biblelib.unit import unit


class TestUnit(object):
    """Test basic functionality for units."""

    def test_unit(self) -> None:
        """Test for unit."""
        testid = "an id"
        empty = unit.Unit(identifier=testid)
        assert empty.identifier == testid
        assert len(empty) == 0
        shortie = unit.Unit((1, 2, 3, 4), identifier=testid)
        assert len(shortie) == 4

    def test_comparison(self) -> None:
        """Test comparison operators"""
        bc0 = unit.Unit(identifier="40002")
        bc1 = unit.Unit(identifier="41002")
        bc2 = unit.Unit(identifier="41003")
        assert bc0 < bc1
        assert bc0 <= bc1
        assert bc0 == bc0
        assert bc0 <= bc0
        assert bc0 != bc1
        assert bc2 > bc1
        assert bc2 >= bc1
