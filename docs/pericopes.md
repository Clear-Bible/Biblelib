# Pericopes

A pericope is a short, conventionalized unit of a Bible
text. Pericopes reflect an analysis of the text into thought units
that are typically larger than a paragraph and smaller than a
chapter.

* Pericopes are a flat list, not hierarchical like an outline.
* Each verse in a Bible is a member of exactly one pericope.
    * Pericopes match verse boundaries.
    * Pericopes do not overlap.
    * Gaps are not allowed.
* Pericopes will largely align with chapter boundaries, but not always.
* Two different `PericopeDict` instances are unlikely to agree in their
  text divisions and pericope names.

## Data Model: PericopeDict

A `PericopeDict` instance vis an ordered collection of `Pericope`
instances from a (localized) Bible edition, e.g. the English NIV2011.

The pericopes are loaded from a TSV file, conventionally named
according to the scheme `pericopes_<LANG>_<VERSION>.tsv`. So the file
with NIV2011 pericopes would be named
`pericopes_eng_NIV2011.tsv`. The versification scheme follows the
version.

The file _must_ have these columns, and values are required for all
columns and rows:
* `startid`: the string representation in BCVID notation of the first verse in the pericope
* `endid`: the string representation in BCVID notation of the last verse in the pericope
* `title`: a brief localized string providing a title for the pericope

The file _may_ have additional columns. If present, they *must* have
distinct names, and values will be added to the `extras` dict on a
`Pericope` instance, where the key is the column name, and the value
is the cell value. Example: for a `PericopeDict` with an additional
`summary` column where the value for the first pericope is "God's
creation of the world", the value of the first `Pericope` instance's
`extras` attribute would be

`{summary: "God's creation of the world"}`


### Attributes

`PericopeDict` inherits usual dictionary attributes.

* `language: str`: an ISO-639 code
* `version: str`: a standardized abbreviation like "NIV2011"
* `license: str`: a standard license identifier. Some pericope sets (like
  NIV2011) may be protected by copyright.
* `path: Path`: the path from which pericope data is loaded.
* `data: dict[int, Pericope]`: a dictionary pairing zero-based index
  numbers with `Pericope` instances.

### Methods

`PericopeDict` inherits usual dictionary methods.

* `eq(other: PericopeDict) -> bool`: two `PericopeDict` instances are equal if
  they have the same language and version.
* `get_pericope(bcvid: BCVID) -> Pericope`: return the pericope that
  contains this verse. Raise ValueError if this verse doesn't occur in
  any pericope.
* `get_pericopes(bcvidrange: BCVIDRange) -> list[Pericope]`: return
  the ordered list of pericopes that intersect with this range of
  verses. Raise ValueError for an empty range or failure to map to a
  sequence of pericopes.
* `get_book_pericopes(bid: BID) -> list[Pericope]`: return the
  complete list of pericopes for this book.

## Data Model: Pericope

A `Pericope` instance describes an individual unit of a Bible text, as
described above. Note that `Pericope` instances do not contain actual
verse text, only references: other code is needed to retrieve textual
content.

### Attributes

* `startid: BCVID`: the BCVID instance for the first verse in the pericope
* `endid: BCVID`: the BCVID instance for the last verse in the pericope
* `title: str`: a brief localized string providing a title for the pericope
* `index: int`: the integer index of this pericope within its parent,
  zero-based.
* `parent: PericopeDict`: the parent to which a `Pericope` belongs.
* `language: str`: the `language` attribute of the parent
* `version: str`: the `version` attribute of the parent
* `book: BID`: the BID instance for the book to which a `Pericope` belongs.

### Methods

* `eq(other: Pericope) -> bool`: two `Pericope` instances are equal if
  they have the same parent and `index`.
* `lt(other: Pericope) -> bool`: a `Pericope` instance is less than
  another one if they have the same parent and the `index` is less.
* `gt(other: Pericope) -> bool`: a `Pericope` instance is greater than
  another one if they have the same parent and the `index` is greater.
* `next() -> Optional[Pericope] `: return the next `Pericope` in the
  sequence, or `None` for the last `Pericope`.
* `previous() -> Optional[Pericope] `: return the previous `Pericope` in the
  sequence, or `None` for the first `Pericope`.
