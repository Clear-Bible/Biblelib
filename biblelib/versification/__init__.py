"""This packages provides information on versification.

The versification is defined by [The Copenhagen Alliance for Open
Biblical Resources](http://copenhagen-alliance.org/). See ReadMe.md
for more details.

"""

from .Mapper import Mapper
from .VrefReader import VrefReader


__all__ = [
    # Mapper
    "Mapper",
    # VrefReader
    "VrefReader",
]
