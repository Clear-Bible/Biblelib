"""Return BCV(WP)ID instances from UBS Marble references.

# this attempts to be smart about failing gracefully if there's no network connection
>>> from biblelib.word import fromubs
>>> fromubs("02306000600008")
[BCVWPID('230600060041')]

"""

from biblelib import has_connection

# requires a network connection
if has_connection():
    from .mappings import Mapper
else:
    print("No internet connection: unable to load Mapper.")

from .bcvwpid import BCVID, BCVWPID


def fromubs(ref: str) -> list[BCVID | BCVWPID]:
    """Return a list of BCV(WP) instances for a single UBS reference.

    Hebrew Bible references sometimes map to two Macula tokens because
    of segmentation differences. Word/part-level references return
    BCVWPID instances based on mapping files. Those without a non-zero
    word index are calculated and return BCVIDs.

    This does not yet handle range references.

    """
    mpr = Mapper()
    macularefs = mpr.to_macula(ref)
    reflist: list[BCVID | BCVWPID] = []
    if macularefs:
        reflist = [BCVWPID(r) for r in macularefs]
    elif ref.endswith("0000"):
        # verse-level reference
        # drop leading digit
        assert ref[0] == "0", f"Leading digit should be 0: {ref}"
        book = ref[1:3]
        chapter = ref[3:6]
        verse = ref[6:9]
        reflist = [BCVID(ID=f"{book}{chapter}{verse}")]
    return reflist
