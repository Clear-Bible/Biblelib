# Biblelib

[![Release](https://img.shields.io/github/v/release/Clear-Bible/Biblelib)](https://img.shields.io/github/v/release/Clear-Bible/Biblelib)
[![Build status](https://img.shields.io/github/workflow/status/sboisen/Biblelib/merge-to-main)](https://img.shields.io/github/workflow/status/sboisen/Biblelib/merge-to-main)
[![codecov](https://codecov.io/gh/sboisen/Biblelib/branch/main/graph/badge.svg)](https://codecov.io/gh/sboisen/Biblelib)
[![Commit activity](https://img.shields.io/github/commit-activity/m/sboisen/Biblelib)](https://img.shields.io/github/commit-activity/m/sboisen/Biblelib)
[![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://sboisen.github.io/Biblelib/)
[![Code style with black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports with isort](https://img.shields.io/badge/%20imports-isort-%231674b1)](https://pycqa.github.io/isort/)
[![License](https://img.shields.io/github/license/sboisen/Biblelib)](https://img.shields.io/github/license/sboisen/Biblelib)

Utilities for working with Bible books, references, pericopes, and
other units. Note this does _not_ include any actual Bible texts.

- **Github repository**: <https://github.com/Clear-Bible/Biblelib
- **Documentation** may *eventually* arrive at
  <https://clear-bible.github.io/Biblelib/> but can be found in the
  `docs` directory, and built using `mkdocs`.

## Installation

```bash
$ pip install biblelib
```

## Usage

### Book metadata

```python
from biblelib.book import Books

books = Books()
books["MRK"]           # <Book: MRK>
books["MRK"].name      # 'Mark'
books["MRK"].osisID    # 'Mark'
books.fromosis("Matt").name      # 'Matthew'
books.frombiblia("Mk").usfmname  # 'MRK'
books.findbook("Ge")             # <Book: GEN>  (searches all schemes)
```

### Rendering Bible references

`BCVID` (book-chapter-verse) and `BCVIDRange` are the primary reference types. Several rendering methods are available:

```python
from biblelib.word import BCVID, BCVIDRange

ref = BCVID("41004003")      # Mark 4:3
ref.to_usfm()                # 'MRK 4:3'
ref.to_nameref()             # 'Mark 4:3'    (full English name)
ref.to_abbrevref()           # 'Mk 4:3'      (biblia abbreviation)
ref.to_osisID()              # 'Mark 4:3'
ref.to_biblia()              # 'Mk 4:3'

rng = BCVIDRange(BCVID("41004003"), BCVID("41004008"))
rng.to_nameref()             # 'Mark 4:3-4:8'
rng.to_abbrevref()           # 'Mk 4:3-4:8'
```

### Localized rendering

`to_nameref()` and `to_abbrevref()` accept an optional `lang` parameter using [ISO 639-3](https://iso639-3.sil.org/) three-letter codes. French (`fra`) is currently bundled; see [Adding a language](#adding-a-language) below for others.

```python
from biblelib.word import BCVID, BCVIDRange

ref = BCVID("01001001")
ref.to_nameref(lang="fra")    # 'Genèse 1.1'
ref.to_abbrevref(lang="fra")  # 'Gn 1.1'

rng = BCVIDRange(BCVID("41004003"), BCVID("41004008"))
rng.to_nameref(lang="fra")    # 'Marc 4.3-4.8'
rng.to_abbrevref(lang="fra")  # 'Mc 4.3-4.8'
```

Note that the chapter-verse separator is language-specific (English uses `:`, French uses `.`).

You can also work with `LocalizedBooks` directly:

```python
from biblelib.book import get_localized_books

fra = get_localized_books("fra")
fra.get_name("GEN")    # 'Genèse'
fra.get_abbrev("GEN")  # 'Gn'
fra.cv_sep             # '.'
```

### Adding a language

Create `biblelib/book/books_<lang>.tsv` (e.g. `books_spa.tsv` for Spanish) with three tab-separated columns and optional metadata comments:

```
# cv_sep: .
usfmname	name	abbrev
GEN	Génesis	Gn
EXO	Éxodo	Éx
...
```

Supported metadata comments:

| Key | Description | Default |
|-----|-------------|---------|
| `cv_sep` | Chapter-verse separator character | `:` |

No code changes are required. The new language is available immediately via `lang="spa"` (or whatever code you used).

## Acknowledgements

* Book abbreviations incorporate public conventions developed by
    * [Unified Standard Format Markers
      3.0.0](https://ubsicap.github.io/usfm/index.html) (USFM), which
      is © Copyright 2018, United Bible Societies.
    * [The Open Scripture Information Standard
      (OSIS)](https://crosswire.org/osis/)
    * [Logos Bible Software](http://www.logos.com/)
* Versification information included consulting sources from:
    * [The Copenhagen Alliance for Open Biblical Resources](http://copenhagen-alliance.org/)
    * [Paratext](https://paratext.org/)
