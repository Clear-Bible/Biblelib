"""Code for mapping between word-level identifiers for various editions."""

from .gnt import GNTMapping, GNTMappings
from .wlcm import WLCMMapping, WLCMMappings
from .marble import Mapper


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
