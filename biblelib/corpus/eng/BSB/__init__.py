"""Corpus analysis of the Berean Standard Bible."""

from pathlib import Path

ROOT = Path(__file__).parent.parent

DATAPATH = ROOT / "data"
ALIGNMENTS = DATAPATH / "alignments"
TARGETS = DATAPATH / "targets"

__all__ = []
