"""Define Unit class."""

from collections import UserList
from enum import Enum
from typing import Any, Optional


class Unit(UserList):
    """Base class for managing units.

    Put things here that are common to all units, whether populated or
    not.

    """

    def __init__(self, initlist: Optional[list] = None, identifier: Any = "(MISSING)") -> None:
        """Instantiate a Unit."""
        super().__init__(initlist)
        # if defined, the parent instance: e.g. parent_chapter of Mark 4:3 is Mark 4
        # each unit should define its own parent types (if any)
        # local, not a class variable, so inheritance works correctly
        self.parent: dict[str, Any] = {}
        # Unique identifier for this unit. All conventional units
        # should have some kind of identifier that supports comparison
        # operators.
        #
        # dunno about arbitrary ranges
        # this is different than a rendered reference: that has a variety of styles
        self.identifier = identifier

    def __repr__(self) -> str:
        """Return a string representation."""
        return f"{type(self).__name__}(identifier={self.identifier})"

    def __lt__(self, other: Any) -> bool:
        """Return true if self < other."""
        return bool(self.identifier < other.identifier)

    def __le__(self, other: Any) -> bool:
        """Return true if self is <= other."""
        return bool(self.identifier <= other.identifier)

    def __eq__(self, other: Any) -> bool:
        """Return true if self == other (same identifier)."""
        return bool(self.identifier == other.identifier)

    def __ne__(self, other: Any) -> bool:
        """Return true if self != other (same identifier)."""
        return bool(self.identifier != other.identifier)

    def __ge__(self, other: Any) -> bool:
        """Return true if self >= other."""
        return bool(self.identifier >= other.identifier)

    def __gt__(self, other: Any) -> bool:
        """Return true if self is > other."""
        return bool(self.identifier > other.identifier)

    # maybe this only makes sense for verse ranges?
    def intersection(self, other: Any) -> set:
        """Return the intersection of self's items and other's.

        Only defined for objects of the same type.
        """
        assert type(self) is type(other), f"intersection not defined for {type(self)} and {other}"
        return set(self.data).intersection(set(other.data))


# maybe these values should be dataclasses that capture
# - description
# - actual data?
# for now, just defines allowable values
class Versification(Enum):
    """Define labels for versification schemes.

    Different versification schemes determine how verse references
    work for a handful of cases. These come from
    https://github.com/Copenhagen-Alliance/versification-specification.

    `eng` may be a reasonable default.

    """

    # Most English and Spanish Bibles.
    ENG = "eng"
    # Septuragint and many Orthodox Bibles
    LXX = "lxx"
    # BHS versfication for OT, UBS GNT for NT
    ORG = "org"
    # "Canonical" (Protestant) edition of the Russian Synodal Bible
    RSC = "rsc"
    # Orthodox (or "non-canonical") edition of the Russian Synodal Bible
    RSO = "rso"
    # Latin Vulgate and translations that use its versification, mainly Catholic Bibles
    VUL = "vul"


def pad(index: int, count: int) -> str:
    """Return a string for index, zero-padded to count characters.

    Use count=2 for books, 3 for chapters and verses.

    """
    return f"{index:{0}{count}}"
