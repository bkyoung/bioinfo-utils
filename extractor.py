#!/usr/bin/env python

import csv, sys, re
from optparse import OptionParser

def listify(r):
    '''
    Convert a string into a list
    '''
    return r.split(',')

def find_column_by_name(line, column_name):
    '''
    Return the index + 1 for a given column header name
    '''
    i = 0
    col_found = False
    for l in line:
        if l.lower() == column_name.lower():
            col_found = True
            column_index = i
        else:
            i += 1
        if col_found == True:
            return str(column_index + 1)
    
    if not col_found:
        raise Exception('Column name ' + column_name + ' was not found.  Please check your spelling.')

def get_columns(line, spec):
    '''
    Returns the specified columns of the line
    '''
    if ":" in spec:
        b = int(spec.split(':')[0]) - 1
        e = int(spec.split(':')[1])
        return line[b:e]
    else:
        c = int(spec) - 1
        return [line[c]]

def match_line(line, match_list):
    '''
    Returns True if all match criteria matched
    '''
    matches = listify(match_list)
    matched = False
    for match in matches:
        c = int(match.split(':')[0]) - 1
        s = match.split(':')[1]
        if line[c] == s:
            matched = True
        else:
            matched = False
            break
    return matched

def extracted_line(line, cl, delimiter):
    '''
    Return the string we will write to file, derived from the specified 
    columns of the supplied line.
    '''
    if cl == None:
        return "{0}\n".format(delimiter.join(line))

    l = []
    column_list = listify(cl)
    for c in column_list:
        l += get_columns(line, c)

    return "{0}\n".format(delimiter.join(l))


if __name__ == '__main__':

    '''
    A simple utility that grabs the specified columns of a TSV file.  If you 
    specify match patterns, only lines that match the string in the specified
    column will be written to the output file.
    '''

    parser = OptionParser()
    parser.add_option("-d", "--delimiter", dest="delimiter", default="\t", help="alternate delimiter (must be a single character.  DEFAULT is a TAB.)")
    parser.add_option("-i", "--infile", dest="inputfile", help="input file name")
    parser.add_option("-o", "--outfile", dest="outputfile", help="output file name")
    parser.add_option("-c", "--columns", dest="columns", 
        help="column numbers to select.  If not specified, all columns will be selected.  EX: 1:6 to select the first 6 columns, or 2:8,15 to select columns 2 - 8 and 15.  You can also say 1:3,9,4:7 to reorder columns in the output file.")
    parser.add_option("-n", "--column-names", dest="columns_by_name", help="columns to select by column header name instead of column number.  This requires that the first line in the file be column headers.  Columns in the output file will apear in the order listed here.")
    parser.add_option("-m", "--match", dest="match", 
        help="column and string to match on.  EX: 2:chr1 to match all lines where column 2 contains 'chr1'.")
    (options, args) = parser.parse_args()
    
    if not options.inputfile:
        parser.error('Input filename not given')

    if not options.outputfile:
        parser.error('Output filename not given')

    if options.match:
        # TODO: Write a regex that allows for optional (',' followed by another match pair)*
        if not re.compile(".+:.+").match(options.match):
            parse.error('Invalid match arguments.  Must look like <int>:<str> (i.e. 2:chr1')

    csv.field_size_limit(sys.maxsize)
    
    with open(options.inputfile, 'r') as infile:
        with open(options.outputfile, 'w') as outfile:
            i = 0
            for line in csv.reader(infile, delimiter=options.delimiter, quoting=csv.QUOTE_NONE ):
                # Always write the first line of the file (column names)
                if i == 0:
                    # First, let's convert named columns to their column number(s)
                    if options.columns_by_name:
                        cbn = options.columns_by_name.split(',')
                        for col in cbn:
                            index = find_column_by_name(line, col)
                            if options.columns:
                                options.columns += ',{}'.format(index)
                            else:
                                options.columns = index
                    outfile.write(extracted_line(line, options.columns, options.delimiter))
                    i += 1
                # If we specified match criteria, only write lines that match
                elif options.match:
                    if match_line(line, options.match):
                        outfile.write(extracted_line(line, options.columns, options.delimiter))
                # If we didn't specify a match criteria, write specified columns for all lines
                elif not options.match:
                    outfile.write(extracted_line(line, options.columns, options.delimiter))
            outfile.close()
        infile.close()