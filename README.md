# Bioinformatics Utilities
This repo contains an ad-hoc collection of utilities for processing data files and extracting desired data.  Expect this repo to evolve over time as new needs arise.

## tsv-extractor.py
This utility can be used to extract the specified columns of a TSV file (tab seperated values).  Further, you can filter on an arbitrary column, thus extracting only lines that match on the specified column and value.  Additionally, the utility supports compund expressions for column and match selectors, as described in the Examples section below.

#### Help Output
```bash
$ ./tsv-extractor.py -h
Usage: extractor.py [options]

Options:
  -h, --help            show this help message and exit
  -i INPUTFILE, --infile=INPUTFILE
                        input file name
  -o OUTPUTFILE, --outfile=OUTPUTFILE
                        output file name
  -c COLUMNS, --columns=COLUMNS
                        columns to select.  If not specified, all columns will
                        be selected.  EX: 1:6 to select the first 6 columns,
                        or 2:8,15 to select columns 2 - 8 and 15
  -m MATCH, --match=MATCH
                        column and string to match on.  EX: 2:chr1 to match
                        all lines where column 2 contains 'chr1'
```

#### Examples
Extract the first six columns from lines in the input file where column 2 matches on "chr1": 
```bash
$ ./tsv-extractor.py -i inputfile.tsv -o outputfile.tsv --cols=1:6 --match=2:chr1
```

Extract columns one through six and thirty, where column two matches 'chr4':
```bash
$ ./tsv-extractor.py -i inputfile.tsv -o outputfile.tsv --cols=1:6,30 --match=2:chr4
```

Extract the first seven columns, but move the seventh column to the fourth position:
```bash
$ ./tsv-extractor.py -i inputfile.tsv -o outputfile.tsv -c 1:3,7,4:6
```

Extract columns thirty folowed by one through six, where column two matches 'chr4' and column eight matches 'rs232':
```bash
$ ./tsv-extractor.py -i inputfile.tsv -o outputfile.tsv -c 30,1:6 -m 2:chr4,8:rs232
```