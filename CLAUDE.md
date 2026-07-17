# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Biblelib is a Python library providing utilities for Bible book metadata, references, versification, and word-level identifiers. It does **not** include any Bible texts. Managed with [Poetry](https://python-poetry.org/).

## Commands

```bash
# Install environment and pre-commit hooks
make install           # poetry install + pre-commit install + poetry shell

# Run all tests (includes doctests in source modules)
make test              # pytest --doctest-modules

# Run a single test file
poetry run pytest tests/unit/test_verse.py

# Run a single test by name
poetry run pytest tests/word/test_bcvwpid.py -k test_fromusfm

# Type checking
make check             # runs mypy

# Build docs locally
make docs              # mkdocs serve

# Build package
make build             # poetry build -> dist/
```

Tests live in `tests/` and mirror the package structure (`tests/book/`, `tests/unit/`, `tests/word/`, `tests/versification/`). Doctests are embedded in source modules and are run as part of `pytest --doctest-modules`.

Code style: **black** (line length 120) + **isort** (black profile). Pre-commit hooks enforce this.

## Architecture

The library is organized into five subpackages:

### `biblelib.book`
Book metadata and collections. Central class is `Books` (a `UserDict`), keyed by USFM 3-letter IDs (e.g. `"MRK"`). Supports lookup by OSIS ID, Logos scheme, and fuzzy name matching via `findbook()`. Data loaded from `books.tsv` at `biblelib/book/books.tsv`.

### `biblelib.unit`
Hierarchical Bible structural units (book, chapter, verse, pericope, ranges). Base class `Unit` (a `UserList`) provides comparison operators via `identifier`. The `Verse` class uses a `BCVID` as its identifier and is keyed to a versification scheme. `UnitRange` supports ranges across units.

### `biblelib.word`
Word-level reference identifiers using the BCVWP format (Book-Chapter-Verse-Word-Part, encoded as `BBCCCVVVWWWP`). Key classes:
- `BID`, `BCID`, `BCVID`, `BCVWPID` — progressively more granular reference identifiers, all dataclasses
- `simplify(inst, target_class)` — reduce granularity (e.g. `BCVWPID` → `BCVID`)
- Class methods `fromusfm()`, `fromlogos()`, `fromtbd()` for parsing various reference schemes
- `biblelib.word.ubs` — maps UBS Marble references to Macula BCVWP IDs (uses the Macula mapping tables, which are downloaded on first use — see `biblelib.data`)
- `biblelib.word.mappings` — mapping files for GNT (`gnt.py`), WLC Morphology (`wlcm.py`), and Marble (`marble.py`). The GNT and Hebrew tables are large and downloaded on demand + cached (`biblelib.data`); loading is lazy, so importing the package triggers no download.

### `biblelib.versification`
Versification support for `eng`, `org`, and `rso` schemes (Protestant canon). `VrefReader` reads `.txt` vref files bundled in `biblelib/versification/`. `Mapper` and `Enumerator` read Copenhagen Alliance scheme JSON also bundled in `biblelib/versification/` (`<scheme>.json`) — all offline, no network. `Enumerator` enumerates verses across a versification and can regenerate the vref files from the bundled JSON.

### `biblelib.corpus`
Currently experimental. Contains `biblelib/corpus/eng/BSB/` (Berean Standard Bible) with a `corpus.py` for SpaCy corpus creation.

### `biblelib.sources`
Enumerates known source Bible editions (`SourceidEnum`: BGNT, NA27, NA28, SBLGNT, WLC, WLCM) and their canons. Top-level `biblelib/__init__.py` exposes `CANONIDS`, `VERSIFICATIONIDS`, and `has_connection()`.

### Localization

Reference rendering supports non-English languages via per-language TSV files at `biblelib/book/books_<lang>.tsv` (e.g. `books_fra.tsv`). The TSV has three columns: `usfmname`, `name`, `abbrev`. Language codes follow ISO 639-3 (e.g. `"fra"`, `"spa"`), matching the existing versification ID convention.

- `LocalizedBooks(lang)` loads a language's data; `get_localized_books(lang)` returns a cached instance
- `BCVID.to_nameref(lang="eng")` → full name reference; `to_abbrevref(lang="eng")` → abbreviated reference
- `BCVIDRange` supports the same `lang` parameter on `to_nameref()` and `to_abbrevref()`
- Adding a new language requires only a new `books_<lang>.tsv` file — no code changes

## Key Conventions

- **USFM 3-letter IDs** are the canonical book identifiers throughout (e.g. `GEN`, `MRK`, `REV`).
- **BCVWP numeric strings** encode references: `BB` book, `CCC` chapter, `VVV` verse, `WWW` word, `P` part. Book numbers follow a specific mapping (not 1-based for all books) — see `books.tsv`.
- The package works offline. The only network use is the on-demand download of the two Macula word-mapping tables (`biblelib.data`, via `pooch`), fetched on first use and cached locally (override the cache dir with `BIBLELIB_DATA_DIR`; pre-seed with `biblelib-download-data`). `has_connection()` is still public but is no longer used internally.
- Mypy is enforced with strict settings (`disallow_untyped_defs`, `disallow_any_unimported`).
