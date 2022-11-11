# Explanation

This part of the project documentation focuses on an
**understanding-oriented** approach. You'll get a
chance to read about the background of the project,
as well as reasoning about how it was implemented.

## Books

### Logos Identifiers

`Book.logosID` identifies Bible books according to the format used by
Logos Bible Software. This is an integer index, starting with 1 for
Genesis, with deuterocanonical books ordered after the Old Testament
(so the index for Matthew is 61, not 40).

### USFM Identifiers

[Unified Standard Format Markers
3.0.0](https://ubsicap.github.io/usfm/index.html) defines three
attributes for identifying a Bible book:

* Number: a two-character string (not actually a number, though the
  most common books use digits). For the early Old Testament books,
  this is zero-padded (so Genesis is "01").
* Identifier:
* English Name:

USFM [Book Identifiers — Unified Standard Format Markers 3.0.0 documentation](https://ubsicap.github.io/usfm/identification/books.html)

---

> **Note:** Expand this section by considering the
> following points:

- Give context and background on your library
- Explain why you created it
- Provide multiple examples and approaches of how
    to work with it
- Help the reader make connections
- Avoid writing instructions or technical descriptions
    here
