# Versification

Different Bible texts encode different choices about

* what books are included in their canon
* the order in which the books appear
* how the verse content is numbered with chapter and verse reference

[The Copenhagen Alliance for Open Biblical
Resources](http://copenhagen-alliance.org/) has identified several
"standard" versification schemes, along with the maximum number of verses in
each chapter compared to a "base" versification scheme, and how to map
from one scheme to another.

The Copenhagen Alliance [defines the following
schemes](https://github.com/Copenhagen-Alliance/versification-specification/tree/master/versification-mappings/standard-mappings):

* `org`: the BHS versification for OT (following Masoretic order), and
  UBS GNT / Nestle-Aland versification for NT.
* `lxx`: The versification used by the Septuagint (LXX) and related
    translations, including most Orthodox Bibles.
* `vul`: The versification used by the Latin Vulgate and translations
  that use its versification, mainly Catholic Bibles.
* `eng`: The versification used by most English (e.g. RSV) and Spanish
  Bibles (e.g. RVR).
* `rsc`: The versification used by the "Canonical" (Protestant)
  edition of the Russian Synodal Bible.
* `rso`: The versification used by the Orthodox (or "non-canonical")
  edition of the Russian Synodal Bible.

(The Copenhagen Alliance formerly also published an `ethiopian_custom`
scheme, but its source is no longer available upstream, so it is not
bundled.)

See the Copenhagen Alliance source for additional details, especially
related to the deuterocanon, and acknowledgements of the contributors.

The Copenhagen Alliance scheme definitions are bundled in this
directory as `<scheme>.json` (`eng`, `org`, `rso` — the schemes in
`biblelib.VERSIFICATIONIDS`), so `Mapper` and `Enumerator` work
offline. To support another scheme, add its `<scheme>.json` here.

The `*-vref.txt` files in this directory *enumerate* the verses
associated with different versification schemes, using USFM
references. They are generated from the bundled `<scheme>.json` files
by `Enumerator.write_enumeration()`, and a test
(`tests/versification/test_vref_derivation.py`) asserts the committed
`.txt` stay byte-identical to that derivation.

> **Do not remove the `*-vref.txt` files.** Biblelib releases up to
> 0.5.4 download them from their raw GitHub URL
> (`.../Clear-Bible/Biblelib/master/biblelib/versification/*-vref.txt`)
> at runtime, so deleting them would break already-deployed clients.
> Current code reads the local copies; the files are kept for
> backward compatibility.

## Other Resources

* The SBL Handbook of Style, Appendix E, contains a table comparing
  English, Hebrew, and Greek versification differences. An older
  version of this is available at
  [7534.Hebrew+English+Bible+Chapter+Verse+Number+Differences.pdf](https://community.logos.com/cfs-file.ashx/__key/CommunityServer.Discussions.Components.Files/77/7534.Hebrew_2B00_English_2B00_Bible_2B00_Chapter_2B00_Verse_2B00_Number_2B00_Differences.pdf)
* Logos Bible Software encodes many different versification schemes
  for individual Bibles as "versemaps". See [Bible Verse
  Maps](https://wiki.logos.com/Bible_Verse_Maps) for further
  information.

## Beyond Versification

In addition to versification schemes, different Bible editions make
choices about which verses are included or omitted, given certain text
critical issues. This extends down to the word level in some cases.

For example, the English Berean Standard Bible omits content associated with ROM
16:24 (though it is acknowledged in a footnote), but includes ROM
16:25-27. The SBLGNT, on the other hand, includes ROM 16:24 but ends
there.

Though both these texts use the same versification scheme, it does not
follow that they include the same verses. This information is not
included in the Copenhagen Alliance data.
