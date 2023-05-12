# Bible Books Data

`books.tsv` incorporates data from
https://ubsicap.github.io/usfm/identification/books.html

The fields are as following:
- Logos Bible datatype number. This supports ordinal sorting
  according to Protestant canon order. Other orders need other support.
- USFM Number (but really a string)
- USFM Identifier
- OSIS ID
- 'standard' English Name
- Long English Name/Alternate names (delimited by '/')

Numerous alternate names in other canons are not included
Order of items here must match properties in Book for loading to
work correctly

Excluded by design:
- Different published Bibles have different names for books
  (e.g. 1SA is '1 Kings' in Douay-Rheims). So 'name' here is a
  conventional one: more data would be required to capture published
  names in other editions.
- Some Clear data has a two-letter abbreviation, perhaps originating
  with Andi Wu (Gen = 'gn', Lev = 'lx', etc. ). Non-normative, so
  excluded.
