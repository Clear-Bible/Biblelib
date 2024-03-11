"""Test code in versification."""

import pytest

from biblelib.versification import VrefReader


class TestVrefReader:
    eng_nt = VrefReader("eng", "nt")
    org_nt = VrefReader("org", "nt")

    def test_init(self) -> None:
        """Test the __init__ method."""
        assert self.eng_nt.scheme == "eng"
        assert self.eng_nt.canon == "nt"
        assert len(self.eng_nt) == 7959
        assert len(self.org_nt) == 7957
        assert self.eng_nt[1187] == "41004009"

    def test_nt_verses(self) -> None:
        """Test versification integrity."""
        assert "44019041" in self.eng_nt
        assert "44019041" not in self.org_nt

    def test_not_asbcv(self) -> None:
        """Test asbcv=False."""
        eng_nt = VrefReader("eng", "nt", asbcv=False)
        assert "ACT 19:41" in eng_nt
        assert "44019041" not in eng_nt
