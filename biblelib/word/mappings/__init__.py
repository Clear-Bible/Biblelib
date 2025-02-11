"""Code for mapping between word-level identifiers for various editions."""

from biblelib import has_connection

from .gnt import GNTMapping, GNTMappings
from .wlcm import WLCMMapping, WLCMMappings

if has_connection():
    from .marble import Mapper
else:
    print("No internet connection: unable to load Mapper.")


__all__ = [
    # mappgins.gnt
    "GNTMapping",
    "GNTMappings",
    # mappgins.wlcm
    "WLCMMapping",
    "WLCMMappings",
    # mappgins.marble
    "Mapper",
]
