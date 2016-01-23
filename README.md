# Bioinformatics Utilities
This repo contains an ad-hoc collection of utilities for fetching, processing data files, and extracting desired data.

## Setup
If you are simply interested in using the utilities, you need only:
 1. Install python 2.7
 2. Ensure the utility is executable (i.e. ```chmod 755 extractor.py```)

## Development
All development of these utilities was done on Mac OS X, in python 2.7.  Every effort has been made to utilize only libraries in the python standard library suite for both normal use and testing/development.

## Utilities
### extractor.py
#### Description
This utility can be used to extract the specified columns of a delimited file.  By default, if no delimiter is specified, tabs are expected, however, you can specify a different delimiter.  You can filter your output on a value in an arbitrary column, thus extracting only lines that match on the specified column and value.  Additionally, the utility supports compound expressions for column and match selectors, as described in the `Usage Examples` section below.  Finally, you may use column header names instead of column numbers to specify which columns to extract.

__NOTE:__ At this time, no effort is made to deduplicate the column list.  If a column is listed multiple times, it will apear that many times in the output file.  It is assumed that the column was listed the number of times it was desired to appear in the output file.

##### Help Output
```bash
$ ./extractor.py -h
Usage: extractor.py [options]

Options:
  -h, --help            show this help message and exit
  -d DELIMITER, --delimiter=DELIMITER
                        alternate delimiter (must be a single character.
                        DEFAULT is a TAB.)
  -i INPUTFILE, --infile=INPUTFILE
                        input file name
  -o OUTPUTFILE, --outfile=OUTPUTFILE
                        output file name
  -c COLUMNS, --columns=COLUMNS
                        column numbers to select.  If not specified, all
                        columns will be selected.  EX: 1:6 to select the first
                        6 columns, or 2:8,15 to select columns 2 - 8 and 15.
                        You can also say 1:3,9,4:7 to reorder columns in the
                        output file.
  -n COLUMNS_BY_NAME, --column-names=COLUMNS_BY_NAME
                        columns to select by column header name instead of
                        column number.  This requires that the first line in
                        the file be column headers.  Columns in the output
                        file will apear in the order listed here.
  -m MATCH, --match=MATCH
                        (optional) column and string to match on.  EX: 2:chr1
                        to match all lines where column 2 contains 'chr1', or
                        'chr1' to match any column containing 'chr1'.  NOTE:
                        multiple values listed together are ANDed together
                        unless --match-mode is used also
  -r, --match-or        Changes matching to OR mode instead of default AND
                        mode
```

##### Usage Examples
Extract the first six columns from lines in the input file where column 2 matches on "chr1": 
```bash
$ ./extractor.py -i inputfile.tsv -o outputfile.tsv --cols=1:6 --match=2:chr1
```

Extract columns one through six and thirty, where column two matches 'chr4':
```bash
$ ./extractor.py -i inputfile.tsv -o outputfile.tsv --cols=1:6,30 --match=2:chr4
```

Extract the first seven columns, but move the seventh column to the fourth position:
```bash
$ ./extractor.py -i inputfile.tsv -o outputfile.tsv -c 1:3,7,4:6
```

Extract columns thirty followed by one through six, where column two matches 'chr4' and column eight matches 'rs232':
```bash
$ ./extractor.py -i inputfile.tsv -o outputfile.tsv -c 30,1:6 -m 2:chr4,8:rs232
```

Extract columns 1 - 6 from a CSV delimited file:
```bash
$ ./extractor.py -i inputfile.tsv -o outputfile.tsv --cols=1:6 --delimiter=,
```

Extract columns named Chr,FuncrefGene,RegulomeCategory2,RegulomeCategory5,GenesWithin60kb:
```bash
$ ./extractor.py -i inputfile.tsv -o outputfile.tsv --column-names=Chr,FuncrefGene,RegulomeCategory2,RegulomeCategory5,GenesWithin60kb
```

Extract all rows where any column matches 'E003':
```bash
$ ./extractor.py -i inputfile.tsv -o outputfile.tsv -m E003
```

Extract all rows where any column matches 'E003' or 'E027':
```bash
$ ./extractor.py -i inputfile.tsv -o outputfile.tsv -m E003,E027
```

Extract all rows where column 3 matches E003 or any column matches 'E027':
```bash
$ ./extractor.py -i inputfile.tsv -o outputfile.tsv -r -m 3:E003,E027
```