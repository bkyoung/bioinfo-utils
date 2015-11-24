# Bioninformatics Utilities
This repo contains an ad-hoc collection of utilities for processing data files and extracting desired data.  Expect this repo to evolve over time as new needs arise.

## extractor.py
This tool can be used to extrac the first six columns of a TSV file (tab seperated values).  Further, you can filter on column 2, thus extracting only lines that match on the specified value in column 2.

### Examples
Extract all lines in the input file where column 2 matches on chromosome 1
```bash
$ ./extractor.py -i inputfile.tsv -o outputfile.tsv -c 1
```
