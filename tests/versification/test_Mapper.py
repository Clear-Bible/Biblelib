"""Test VrefReader()."""

import pytest

from biblelib.versification import Mapper


class TestMapper:
    """Test Mapper()."""

    mapper = Mapper("eng", "org")

    def test_init(self) -> None:
        """Test initialization."""
        assert self.mapper.fromscheme == "eng"
        assert self.mapper.toscheme == "org"

    def test_load_scheme(self) -> None:
        """Test _load_scheme()."""
        fromschemejson = self.mapper._load_scheme("eng")
        assert len(fromschemejson) == 4
        assert fromschemejson["mappedVerses"]["2SA 19:1-43"] == "2SA 19:2-44"
        assert len(fromschemejson["excludedVerses"]) == 0
        assert len(fromschemejson["partialVerses"]) == 0
        # toschemejson = self.mapper._load_scheme("org")
        # assert toschemejson["verses"]["GEN"]["1"] == "31"
        with pytest.raises(AssertionError):
            _ = self.mapper._load_scheme("foo")
