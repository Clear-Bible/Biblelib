"""This package provides pericope data for Bible texts.

A pericope is a short, conventionalized unit of Bible text. Each verse
belongs to exactly one pericope within a given edition's pericope set.
"""

from .pericope import Pericope, PericopeDict

__all__ = [
    "Pericope",
    "PericopeDict",
]
