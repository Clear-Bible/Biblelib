"""Test word.reference"""

from biblelib.word import urlmanager

# import pytest

from biblelib.word import BCID, BCVID, BCVIDRange

# from biblelib.word import frombiblia, fromlogos, fromname, fromosis, fromusfm, simplify, to_bcv, make_id, is_bcvwpid


class Test_URLManager:
    """Test URLManager()."""

    urlmgr = urlmanager.URLManager()

    def test_biblecom(self) -> None:
        """Test generating URLs for the default, bible.com."""
        bcvref = BCVID("41004003")
        assert self.urlmgr.netloc == "bible.com"
        assert self.urlmgr.edition == "NIV"
        assert self.urlmgr.get_uri(bcvref=bcvref) == "https://bible.com/bible/111/MRK.4.3"

    def test_biblecom_chapter(self) -> None:
        """Test generating chapter URLs for the default, bible.com."""
        bcvref = BCID("41004")
        assert self.urlmgr.get_uri(bcvref=bcvref) == "https://bible.com/bible/111/MRK.4"

    def test_biblecom_verserange(self) -> None:
        """Test generating verse range URLs."""
        startref = BCVID("41004003")
        endref = BCVID("41004009")
        bcvref = BCVIDRange(startref, endref)
        assert self.urlmgr.netloc == "bible.com"
        assert self.urlmgr.edition == "NIV"
        assert self.urlmgr.get_uri(bcvref=bcvref) == "https://bible.com/bible/111/MRK.4.3-9"

    # should test that it fails on unsupported cases
