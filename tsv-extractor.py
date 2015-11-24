#!/usr/bin/env python

import csv, sys, re
from optparse import OptionParser

def s_to_a(r):
    '''
    Convert a string into a list
    '''
    return r.split(',')

def column_range(r):
    '''
    Converts column range into meaningful values for a slice
    EX: 2:6 at the command line results in a slice of [1:6]
    '''
    b = int(r.split(':')[0]) - 1
    e = int(r.split(':')[1])
    return (b, e)

def get_columns(line, spec):
    '''
    Returns the specified columns of the line
    '''
    if re.compile("^.+:.+$").match(spec):
        b, e = column_range(spec)
        return line[b:e]
    else:
        return [line[int(spec) - 1]]

def match_pair(m):
    '''
    Returns column and string to search for in a line
    '''
    c = int(m.split(':')[0]) - 1
    s = m.split(':')[1]
    return (c, s)

def match_line(line, match_list):
    '''
    Returns True if all match criteria matched
    '''
    matches = s_to_a(match_list)
    matched = False
    for match in matches:
        c, m = match_pair(match)
        if line[c] == m:
            matched = True
        else:
            matched = False
            break
    return matched

def writeln(line, column_list):
    '''
    Return the string we will write to file, derived from the specified 
    columns of the supplied line.
    '''
    l = []
    cl = s_to_a(column_list)
    for c in cl:
        l += get_columns(line, c)

    return "{0}\n".format("\t".join(l))


if __name__ == '__main__':

    '''
    A simple utility that grabs the specified columns of a TSV file.  If you 
    specify match patterns, only lines that match the string in the specified
    column will be written to the output file.
    '''

    parser = OptionParser()
    parser.add_option("-i", "--infile", dest="inputfile", help="input file name")
    parser.add_option("-o", "--outfile", dest="outputfile", help="output file name")
    parser.add_option("-c", "--columns", dest="columns", 
        help="columns to select.  If not specified, all columns will be selected.  EX: 1:6 to select the first 6 columns, or 2:8,15 to select columns 2 - 8 and 15")
    parser.add_option("-m", "--match", dest="match", 
        help="column and string to match on.  EX: 2:chr1 to match all lines where column 2 contains 'chr1'")
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
            for line in csv.reader(infile, delimiter='\t', quoting=csv.QUOTE_NONE ):
                # Always write the first line of the file (column names)
                if i == 0:
                    outfile.write(writeln(line, options.columns))
                    i += 1
                # If we specified match criteria, only write lines that match
                elif options.match:
                    if match_line(line, options.match):
                        outfile.write(writeln(line, options.columns))
                # If we didn't specify a match criteria, write all lines
                elif not options.match:
                    outfile.write(writeln(line, options.columns))
            outfile.close()
        infile.close()