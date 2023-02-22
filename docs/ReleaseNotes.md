# Release Notes

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
