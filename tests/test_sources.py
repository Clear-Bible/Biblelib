"""Pytest tests for biblelib.unit."""

import pytest


from biblelib import sources


class TestSourceidEnum:
    """Test SourceidEnum()."""

    def test_SourceidEnum(self) -> None:
        """Test initialization."""
        assert sources.SourceidEnum("SBLGNT").value == "SBLGNT"
        # error on unrecognized sources
        with pytest.raises(ValueError):
            assert sources.SourceidEnum("foo").value == "foo"

    def test_get_canon(self) -> None:
        """Test get_canon()."""
        assert sources.SourceidEnum.get_canon("BGNT") == "nt"
        assert sources.SourceidEnum.get_canon("NA28") == "nt"
        assert sources.SourceidEnum.get_canon("SBLGNT") == "nt"
        assert sources.SourceidEnum.get_canon("WLC") == "ot"
        assert sources.SourceidEnum.get_canon("WLCM") == "ot"
        assert sources.SourceidEnum.get_canon("foo") == "X"

class TestEdition:
    """Test Edition() dataclass."""

    def test_Edition(self) -> None:
        """Test initialization."""
        edition = sources.Edition("SBLGNT", "nt", "grc")
        assert edition.sourceid == "SBLGNT"
        assert edition.canon == "nt"
        assert edition.language == "grc"

    def test_from_sourceid(self) -> None:
        """Test from_sourceid()."""
        edition = sources.Edition.from_sourceid("SBLGNT")
        assert edition.sourceid == "SBLGNT"
        assert edition.canon == "nt"
        assert edition.language == "grc"
        edition = sources.Edition.from_sourceid("WLC")
        assert edition.sourceid == "WLC"
        assert edition.canon == "ot"
        assert edition.language == "hbo"
        with pytest.raises(ValueError):
            edition = sources.Edition.from_sourceid("foo")
