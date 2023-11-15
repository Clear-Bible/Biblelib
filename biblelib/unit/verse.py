"""Define Verse class.

This code is under-developed, but is intended for identifying verses
as units. For managing BCV references, see biblelib.word.bcvwpid
instead.

>>> from biblelib.unit import verse
>>> verse.Verse(verse.BCVID("41004003"))
Verse(identifier='BCVID('41004003')')

"""

from typing import Any, Optional

from biblelib.word import BCVID
from .unit import Unit, Versification


class Verse(Unit):
    """Manage Verse units.

    The scheme for identifying verses is BCV (no word or part index):
    these identifiers are used for comparison.

    A Verse instance has a data attribute for consistency, but it's
    not currently populated.

    A versification attribute indicates how the identifiers should be
    interpreted: only the default of the 'eng' scheme for now, and not
    actually used yet.

    """

    # if defined, the parent instance: e.g. parent_chapter of Mark 4:3 is Mark 4
    # could also be parent sentence, paragraph, pericope ... so dict for extensibility
    parent: dict[str, Any] = {"Chapter": None}

    def __init__(
        self, inst: Optional[BCVID], initlist: Optional[list] = None, versification: Versification = Versification.ENG
    ) -> None:
        """Instantiate a Verse."""
        super().__init__(initlist=initlist, identifier=inst)
        self.inst = inst
        assert isinstance(inst, BCVID), f"Inst must be a BCVID instance: {inst}"
        assert versification in Versification, f"Invalid versification: {versification}"
        self.versification = versification
