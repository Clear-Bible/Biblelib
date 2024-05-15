# Release Notes

## 0.3.8

- Added `make_id()` method to `word.bcvwpid` to return an instance of
  whatever class matches the length of the reference string (BID,
  BCID, BCVID, BCVWPIP).


## 0.3.7

- Added `get_id()` method to `word.bcvwpid.BCVID` for consistency with
  `BCVWPID`. This allows calling the same method on a list of
  references that mixes verse-level and word/part level.

## 0.3.6

- Refactored BCVWPID.get_id() with better logic, but a breaking change:
    - Default is now no canon prefix, the opposite of previous
      version. Writing Macula-matching data should set prefix=True.
    - Default is to output the part index (so Greek and targets should
      set part_index=False)
    - Canon prefix is no longer part of the `ID` value.
    - Tests updated to match.

## 0.3.5

- Better handlings of UBS MARBLE references. Now using the Macula
  mapping tables for Hebrew and Greek references at the word level,
  and otherwise converting to a BCVID.
    - This deprecates word/mappings in favor of a `word.mappings`
      module.

## 0.3.4

- Added word.bcvwpid.BCVIDRange to handle within-chapter ranges, just
  as references. Note this does not yet handle cross-chapter ranges:
  that requires knowledge of the Verse contents, which bcvwpid doesn't
  have. Future work.
- Added enumerate_ids() to unit.unitrange.VerseRange()
- Additional tests

## 0.3.3

- Added book.frombiblia() and tests. Added biblia identifiers to books.tsv.
- Moved to_bid/bcid/bcvid upward in the class hierarchy in bcvwpid,
  with updated tests.
- added `ID`, `book` and `chapter` attributes to `VerseRange`.
- Fixed some type hints in book/book.py. Added bibliaURI for
  generating links to online text.
- VrefReader now checks `scheme` and `canon` validity.

## 0.3.2

- Added constants for source languages and versions, and support for
  Bible editions.
- Added to_bcv to bcvwpid for the frequent use case of converting to a
  simple book-chapter-verse reference.
- Initial support for versification: work is ongoing.

## 0.3.1

- Handling of OSIS references was all wrong: now fixed.

## Minor version update: 0.3.0

Added "vref" versification data:
`[eng|org|rso]-[nt|ot|protestant]-vref.txt` files enumerate the verses
(with USFM references) for `eng` and `org` versification schemes,
respectively, with subsets for NT, OT, and Protestant canon (excluding
Deuterocanon).

Also added support for generating these files from [The Copenhagen
Alliance for Open Biblical
Resources](http://copenhagen-alliance.org/), with data from
https://github.com/Copenhagen-Alliance/versification-specification. While
a complete set of vref files isn't yet included,
`versification.Enumerator` can be used to generate them.

More details are in `versification/ReadMe.md`.

## 0.2.28

- Another bug fix for word.fromubs() and note links:
  "04400705400018({N:001})".
- use zfill.

## 0.2.27

- Fixed bugs in word.fromubs() to strip off note links (e.g.,
  "04400705400018{N:001}") and treat odd-numbered word indices.

## 0.2.26

- Fixed a subtle bug with unit.parent: was a class variable instead of
  local.
- bug fix for word.pad3 to correctly handle "0" as input
- refactored tests to reflect source code hierarchy

## 0.2.25

- Updated upper end of Python requirement to `<4` and updated
  packages.

## 0.2.24

- Fixes to unitrange.py. I had the logic wrong: now both *Range
  classes return a list of Units from their enumerate() methods
  (ChapterRange -> list[Chapter], same for VerseRange).
- Changed start/end to startid/endid for clarify.
- Updated tests to correspond. Added test_invalid_comparison to
  test_unit.py.

## 0.2.23

- realized it was dumb to name a module `range`: now `unitrange`.
- Fixed issues with imports in `biblelib.unit`; added `unitrange` to
  exported variables
- Other fixes to avoid circular imports


## 0.2.22

- Breaking changes for `bcvwpid.BCVWPID` output: now use `get_id()` to
  return an identifier string, which now has a corpus prefix ("o" for
  OT, "n" for NT). Also, NT tokens now have no part
  identifier. Parameters to `get_id()` can modify this behavior for
  backward compatibility.
- Can now initialize `bcvwpid.BCVWPID` with a corpus prefix. The
  corpus prefix is defined whether supplied on initialization or not.
- Two Greek instances compare as equal even if only one is initialized
  with a word part = "1".
- You can now product the reduced identifier for a `BCVWPID` instance
  with new properties `to_bid`, `to_bcid`, and `to_bcvid`.

## 0.2.21

- Added support for chapter and verse ranges.
- Added support for Macula canon prefix for BCVWPID identifiers ("o"
  for Old Testament, "n" for New Testament, otherwise "x").
- Messed up and missed 0.2.20.

## 0.2.19

- Refactored `unit.Unit` and subclasses (Book, Chapter, Verse) for
  clearer parameter names. Tests updated to match.
- Fixed a bunch of type hint complains and mismatches

## 0.2.18

- added `word.bcvwpid.fromubs()` to convert from 14-character
  references to `BCVWPID`
- generalized Python version for future-proofing
- a few other fixes

## 0.2.17

- Bug fix to `bcvwpid.simplify()`: need to handle class *types*, not names.

## 0.2.16

- Bug fix to `hash()` for unit types. They don't get inherited from
  `_Base` without `unsafe_hash=True`.

## 0.2.15

- Add base class `_Base` to simplify the code.

## 0.2.14

- Add `includes()` to `word.bcvwpid` for all unit types (BID, BCID,
  BCVID, BCVWPID). This allows testing whether one unit is included in
  another, larger one.

  ```
  # is Mark 4:8 in Mark?
  >>> BID("41").includes(BCVID("41004008"))
  True
  # is Matt 1 in Mark?
  >>> BID("41").includes(BCID("40001"))
  False
  ```

## 0.2.13

- Bug fix/extension: handle "Psalm" and "Song of Solomon" as book
  names. This takes a little hackery that isn't very extensible: it's
  not a general solution to the alternate names issue.

## 0.2.12

- Bug fix: book name for Esther in books.tsv was non-standard,
  causing an error with bcvwpid.fromname.

## 0.2.11

- Added `simplify()` method to bcvwpid. Expanded to_usfm to other
  classes. Added test cases.

## 0.2.10

- Added `to_usfm` to word.bcvwpid.BCVID so references can be
  round-tripped back to USFM style (e.g., "41004008" -> "MRK 4:8").

## 0.2.9

- Added bcvwpid.fromname() and nameregexp for full-name matching:
  hacks don't cut it here.

## 0.2.8

- Bug fix to "2Cor" capitalization in books.tsv.

## 0.2.7

- Bug fix in fromosis().

## 0.2.6

- Add fromosis and fromusfm to bcvwpid, along with tests.

## 0.2.5

- Added `unit` module for structures below the book.
- Pulled documentation on books.tsv into its own file.
- Added tests.
- Module renames: words -> word, books -> book.
- Added versification data.
- Delete words/mappings.

## 0.2.4

- Renamed "Clear ID" to "BCVWP ID" throughout.

## 0.2.3

- Bug fix: USFM numbers for single-digit OT books like Genesis are now
  correctly zero-padded (e.g., "01").
- Bug fix: missing altnames are now "" (per documentation) rather than `None`.
- Added tests.

## 0.2.2

- Bug fix: words.ClearID() now correctly reports an invalid ID. Added
  testing to ensure exceptions are raised for invalid ID length.

## 0.2.1

- Bug fixes for words.ClearID and tests/test_clearid.
- Bug fixes for tests/test_mappings.py
