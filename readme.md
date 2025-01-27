# PDFSplit

## Summary
A small DSL[1] transcodes user-specified tags to specific pages of a PDF
into sqlite database.

DSL Schema per line
<page>(,<page>)?: <tag> (, <tag)*
eg.
1-3: "introduction", "commentary"
8: "conclusion"

Each PDF is split using pdftoppm[2] and each page rendered as png before conversion to base64
SQLite DB structure can read in 'sql/schema.sql'

## Options
--pdf-loc (defaults to 'pdfs') - Location of PDFs
--dsl-loc (defaults to 'parsers') - Location of .lark files corresponding to the same path as the respective PDF
For example :
/pdfs/foo/bar/example.pdf
will require a parser at
/parsers/foo/bar/example.lark
--db-loc (defaults to 'output.db') - Location of output SQLite database
--meta-loc (defaults to 'metadata.json') - [Depreciation Warning!]
Any additional data corresponding to a unique PDF name can be loaded via a JSON file

--overwrite (defaults to 'False') - Determines if existing database should be overwrote

## References
[1] Domain Specific Language : See https://lark-parser.readthedocs.io/
[2] pdftoppm : See https://manpages.debian.org/testing/poppler-utils/pdftoppm.1.en.html 
