# How-To Guides

## Books

For all the items in this section, begin with

```
>>> from biblelib import books
>>> allbooks = books.Books()
```


### Convert a USFM Book Name to an OSIS Identifier

```
>>> allbooks["MRK"].osisID
'Mark'
```

### Convert a USFM Book Number to a USFM Name

```
>>> allbooks.fromusfmnumber("41").usfmname
'MRK'
```

### Render the Longer Name for a Book

```
>>> allbooks["ZEC"].render("name")
'Zechariah'
```

### Generate the Logos URI for a Book Instance

```
>>> allbooks["MRK"].logosURI
'https://ref.ly/logosref/bible.62'
```

### Enumerate the Book Identifiers for the Protestant Canon

```
>>> list(books.ProtestantCanon())

['GEN', 'EXO', 'LEV', 'NUM', 'DEU', 'JOS', 'JDG', 'RUT', '1SA', '2SA',
'1KI', '2KI', '1CH', '2CH', 'EZR', 'NEH', 'EST', 'JOB', 'PSA', 'PRO',
'ECC', 'SNG', 'ISA', 'JER', 'LAM', 'EZK', 'DAN', 'HOS', 'JOL', 'AMO',
'OBA', 'JON', 'MIC', 'NAM', 'HAB', 'ZEP', 'HAG', 'ZEC', 'MAL',
'MAT', 'MRK', 'LUK', 'JHN', 'ACT', 'ROM', '1CO', '2CO', 'GAL', 'EPH',
'PHP', 'COL', '1TH', '2TH', '1TI', '2TI', 'TIT', 'PHM', 'HEB', 'JAS',
'1PE', '2PE', '1JN', '2JN', '3JN', 'JUD', 'REV']
```
