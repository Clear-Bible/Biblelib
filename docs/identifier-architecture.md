# Identifier Architecture

How Biblelib makes references from different systems commensurable, what
survives normalization, and what does not.

This is an understanding-oriented document. It describes the design as
implemented, and marks observations about gaps as observations rather than
commitments.

## What the library is for

Biblelib is a **reference-identity layer**. The problem it solves is that the
same verse has a different name in every system — USFM, OSIS, Logos, Biblia,
Paratext, Macula, UBS Marble, Tyndale Bible Dictionary markup, plus a dozen
natural languages — and different Bibles do not even agree on which verse it
is. Biblelib makes those names commensurable.

It is worth stating what the library is *not*, because the BCVWP focus invites
a wrong guess: **Biblelib is not an alignment library.** It contains no
alignment data and no alignment algorithm. The string "alignment" appears twice
in the tree, and neither occurrence is functionality — one sentence in
`docs/pericopes.md` about pericopes aligning with chapter boundaries, and an
unused `ALIGNMENTS` path constant in the experimental corpus module
(`biblelib/corpus/eng/BSB/__init__.py:8`).

Alignment work uses Biblelib heavily because alignment data is keyed by Macula
BCVWP identifiers. That makes alignment a downstream consumer, not the purpose.

Substantial functionality has nothing to do with alignment:

* **Versification mapping** (`biblelib/versification/`) — mapping references
  between `eng`, `org`, and `rso`, including the places where Bibles genuinely
  disagree about verse boundaries.
* **Pericopes** (`biblelib/pericope/`) — titled units of text with ordering and
  navigation; every verse belongs to exactly one pericope per edition.
* **Localized rendering** — 19 bundled languages, including per-language
  chapter/verse separators.
* **Structural units and ranges** (`biblelib/unit/`) — containment and
  comparison over books, chapters, verses.
* **URL generation** (`biblelib/word/urlmanager.py`) — bible.com deep links
  from a reference.

## Three mechanisms, not one

Identifiers are made commensurable by three different designs. Which one
applies determines what happens to the identifier you supplied.

### 1. Table rows — books and word-level editions

For book names and for Greek New Testament words, every system's identifier
sits side by side as parallel columns on one row. Nothing is converted, so
nothing is lost: the row *is* the correspondence.

`biblelib/book/books.tsv`:

```
logosID | usfmnumber | usfmname | osisID | biblia | name | altname
```

`GNTMapping` (`biblelib/word/mappings/gnt.py:62-74`) holds seven parallel
fields per row — `NA1904_ID`, `NA1904_Text`, `NA27_ID`, `NA28_ID`, `SBLGNT_ID`,
`SBLGNT_Text`, `MARBLE_ID`.

`Books.fromosis()`, `.frombiblia()`, `.fromlogos()`, `.fromusfmnumber()` are
indexed lookups into that row, not transformations. This is why `findbook()`
can search every scheme at once, and why a new naming scheme means a new
column rather than new code.

**Consequence: books and GNT words are fully round-trippable.**

### 2. Hub and spoke — the reference classes

The numeric `BBCCCVVVWWWP` string is the pivot format. Every `from*` function
parses an external notation into it; every `to_*` method renders back out.

```
USFM  ─┐                                  ┌─ to_usfm()
OSIS  ─┤                                  ├─ to_osisID()
Logos ─┼─→  BID / BCID / BCVID / BCVWPID ─┼─ to_biblia()
Biblia─┤    (BBCCCVVVWWWP)                ├─ to_nameref(lang=)
TBD   ─┘                                  └─ to_abbrevref(lang=)
```

Parsers are at `biblelib/word/bcvwpid.py:831-1074`; renderers at
`:165-562`. The classes form an inheritance chain of increasing granularity,
`BID` → `BCID` → `BCVID` → `BCVWPID`, with `BCVIDRange` alongside.

This is a star topology: N parsers plus N renderers rather than N² pairwise
converters, and adding a notation touches nothing existing.

**Consequence: the round trip is lossy at the surface.** See "What survives
normalization" below.

### 3. Pairwise data — versification

Versification is deliberately *not* hubbed. `Mapper(fromscheme, toscheme)`
loads only the source scheme's JSON (`biblelib/versification/Mapper.py:39-45`)
and uses Copenhagen Alliance standard-mappings data directly.

### 4. Lookup tables — cross-resource word identity

`fromubs()` → `Mapper.to_macula()` (`biblelib/word/ubs.py:13-28`) is a table
hit against downloaded data, not a computation. It returns a *list*, because
one UBS Marble reference can map to two Macula tokens where Hebrew segmentation
differs. This mapping is not computable, which is why the 12 MB tables exist.

## Versification is separate from reference identity

This is the sharpest edge in the design, and it is intentional.

`BCVID` carries no versification scheme. Versification is mentioned exactly
once in `bcvwpid.py`, in a comment about maximum chapter count (line 284). So a
reference parsed from an `eng` Bible and the same reference parsed from an
`org` Bible produce **identical, indistinguishable** `BCVID` instances.

`unit.Verse` does have a `versification` attribute, but its own docstring says
it is "not actually used yet" (`biblelib/unit/verse.py:30`).

The consequence is worth stating plainly:

> The hub tells you two references have the same **name**. It does not tell you
> they point at the same **text**.

Those are separate questions, and the library keeps them separate. Code that
needs the second question answered must go through `Mapper`.

## What survives normalization

### Table rows: the original is kept, permanently

Every column is present on the row. Nothing to recover, because nothing was
discarded.

### Reference objects: the original is discarded

`_Base` has exactly three fields — `ID`, `book_ID`, `_idlen`
(`bcvwpid.py:86-94`). There is no source field and nowhere to put one.

```python
fromusfm("Gen 3:16")           # → BCVID('01003016')   — "Gen 3:16" is gone
BCVID('01003016').to_usfm()    # → 'GEN 3:16'          — a USFM rendering, not yours
```

`Gen` comes back as `GEN`. The renderer is behaving correctly — it emits the
canonical shape — but the input is not recoverable.

The lossy dimensions at this level are unbounded, not binary:

* **which scheme** it came from (`fromusfm`, `fromosis`, `fromname`,
  `frombiblia`, `fromlogos`, `fromtbd` all land on the same `BCVID`, which
  retains no trace of which)
* **case** — `from_usfm` does `BOOKS[bookabbrev.upper()]` (`bcvwpid.py:941`),
  so `Gen`, `gen`, `GEN` collapse
* **padding** — `pad3()` normalizes `3` and `003`
* **which name form** — `Matt`, `Matthew`, `Mt` are different columns that
  converge on one result

### `BCVWPID`: recoverable, via reconstruction rather than storage

The `source_id` property (`bcvwpid.py:676-695`) returns the identifier exactly
as supplied:

```python
BCVWPID("n40001001001").source_id   # 'n40001001001'
BCVWPID("n40001001001").get_id()    # '400010010011'
```

The implementation detail that matters: **it does not store the original
string.** It stores two booleans and reconstructs.

```python
strid = self.ID if self._had_part_ID else self.ID[:-1]
return f"{self.canon_prefix}{strid}" if self._had_canon_prefix else strid
```

`_had_canon_prefix` and `_had_part_ID` (`bcvwpid.py:621-622`) are declared
`field(init=False, default=False, compare=False, repr=False)`. The
`compare=False` is the important discipline: these record *how an identifier
was written*, not *which word it denotes*, so two identifiers for the same word
remain equal when one was supplied with a prefix and the other without.

This works because `BCVWPID`'s normalization is exactly two binary facts:
prefix present or not, part index present or not. Four states of input, four
states of memory. It costs nothing per instance, which matters because
`BCVWPID` is the class materialized by the million when a word-level corpus is
loaded.

### Why the motivating case was real

Identifiers belong to whoever published the text they point into. Code
integrating data from several sources has to hand back the identifier it was
given, or its output no longer resolves against the source it came from. Before
`source_id`, `BCVWPID` normalization dropped a supplied canon prefix and
appended a part index that was never there, and `get_id()`'s flags could not
recover either, because by the time they are read the truth about the input is
gone.

## Whether `BCVID` needs the same treatment

The `BCVWPID` solution does not generalize, because the input space one level
up is unbounded rather than four-valued. Recovering it would require storing
the actual input string on the instance.

The mechanism is proven and would be straightforward: add
`_source: str = field(default="", init=False, compare=False, repr=False)` to
`_Base` and all four classes inherit it, with the same `compare=False`
discipline leaving equality and ordering untouched. The parsers are
module-level functions, so they can set it after construction. It is not hard.
It is simply not free the way the `BCVWPID` fix was.

There is a mild irony in the economics: the cheap fix went to the class you
hold millions of, and the class you would only ever hold thousands of is the
one that would need the expensive one. The cost argument cuts toward doing it,
not away.

### The question that decides it

**Is the notation a property of the channel, or of the record?**

*Channel.* If a pipeline reads OSIS references and writes OSIS references, the
notation is already known. Parse at the boundary, work in the hub, call
`to_osisID()` on the way out. Per-instance source tracking is dead weight and
one line at the edge does the whole job.

*Record.* The `BCVWPID` case was genuinely different, which is why the fix was
warranted there: the variation arrives per record, within a single notation,
from sources that disagree with each other about whether to write the prefix.
That cannot be hoisted to the channel, because the channel is mixed.

So the test is: **do you ever hold a collection of references that came from
different notations and have to hand each one back the way it arrived?** If
every reference in a given file or feed shares a notation, per-instance source
tracking is unnecessary. If you are merging feeds and echoing references into
output that a third party resolves against their own source, it is not.

## Observed asymmetries

These are observations about the current state, not a roadmap.

### Input-only spokes

The renderers are `to_usfm`, `to_osisID`, `to_biblia`, `to_nameref`,
`to_abbrevref` (plus the internal `to_bid` / `to_bcid` / `to_bcvid` and
`to_format`). There is **no `to_logos()` and no `to_tbd()`**. Logos identifiers
and Tyndale markup can be parsed *in* but not emitted *out*.

This matters for the channel strategy above: if something downstream must
return a Logos-style reference, there is no renderer to call at the boundary.
Closing it would be a lookup — `logosID` is already a column in `books.tsv`.

### Directional mapping functions

The word-mapping tables are bidirectional as *data* — every row carries every
column — but only one direction is implemented as code:

* `marble2sblgnt()` (`mappings/gnt.py:121`)
* `na282sblgnt()` (`mappings/gnt.py:141`)
* `marble2macula()` (`mappings/wlcm.py:91`)
* `to_macula()` (`mappings/marble.py:40`)

There is no `macula2marble()` or `sblgnt2na28()` index. `to_marble_id` reaches
the Marble identifier if you already hold the row, but not if you are starting
from a Macula identifier.

### Parser input tolerance

`from_usfm` requires range ends to be fully specified —
`assert ":" in endref` (`bcvwpid.py:950`) — so `MRK 4:3-8` raises rather than
parsing as `MRK 4:3-4:8`. For some real-world USFM input the question is not
whether the notation can be reproduced, but whether it can be ingested at all.

## Summary

Originals are kept where the design is a table, dropped where the design is a
hub, and `source_id` adds a keyhole for the one hub case where dropping them
was breaking integration. Whether the `BCVID` case needs the same treatment
depends on whether the notation is a property of the channel or of the record.
