import pytest
from biblelib.versification.Enumerator import Enumerator


from biblelib import has_connection


class TestEnumerator:
    enumerator = Enumerator("org")

    def test_init(self) -> None:
        """Test the __init__ method."""
        if not has_connection():
            print("Cannot load Enumerator without network connection.")
            exit()
        assert self.enumerator.scheme == "org"
        assert (
            self.enumerator.mappingfile
            == "https://raw.githubusercontent.com/Copenhagen-Alliance/versification-specification/master/versification-mappings/standard-mappings/org.json"
        )
        assert self.enumerator.versedict["excludedVerses"] == []
        assert self.enumerator.versedict["partialVerses"] == {}

    def test_books(self) -> None:
        """Test the books method."""
        books = self.enumerator.books()
        assert len(books) == 95
        assert books[0] == "GEN"
        assert books[65] == "REV"

    def test_nt_books(self) -> None:
        """Test books(nt_only=True)"""
        nt_books = self.enumerator.books(nt_only=True)
        assert len(nt_books) == 27
        assert nt_books[0] == "MAT"
        assert nt_books[-1] == "REV"

    def test_ot_books(self) -> None:
        """Test books(ot_only=True)"""
        ot_books = self.enumerator.books(ot_only=True)
        assert len(ot_books) == 39
        assert ot_books[0] == "GEN"
        assert ot_books[-1] == "MAL"

    def test_protestant_books(self) -> None:
        """Test the books method."""
        books = self.enumerator.books(with_deuterocanon=False)
        assert len(books) == 66
        assert books[0] == "GEN"
        assert books[-1] == "REV"

    def test_chapters(self) -> None:
        """Test chapter length."""
        chapters = self.enumerator.versedict["maxVerses"]["MRK"]
        assert len(chapters) == 16

    def test_chapter_verses(self) -> None:
        """Test chapter verses."""
        n_verses = self.enumerator.chapter_verses("MRK", 1)
        assert n_verses == 45

    def test_enumerate_verses(self) -> None:
        """Test enumerate_verses."""
        verses = self.enumerator.enumerate_verses("MRK", 1)
        assert len(verses) == 45
        assert verses[0] == "MRK 1:1"


# should add tests for other versification schemes
