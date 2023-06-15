# Release Notes

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
