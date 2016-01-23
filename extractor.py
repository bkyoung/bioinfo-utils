#!/usr/bin/env python

import csv, sys, re
from optparse import OptionParser

def listify(r):
    '''
    Convert a comma delimited string into a list

    Accepts:
        r: a string containing commas

    Returns: a list
    '''
    return r.split(',')

def find_column_by_name(line, column_name):
    '''
    Return the index + 1 for a given column header name

    Accepts:
        line: a list
        column_name: a string to search for in line

    Returns: a string representing the index of the column being searched for
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
        raise Exception(
            'Column name "' + column_name + '" was not found.  Please check your spelling.')

def get_columns(line, spec):
    '''
    Returns the specified columns of the line

    Accepts:
        line: a list
        spec: a string containing a column index or : separated range of columns

    Returns: a list containing the specified columns
    '''
    if ":" in spec:
        try:
            b = int(spec.split(':')[0]) - 1
        except:
            raise Exception(
                "When specifying column numbers, they must be integers: '"
                + spec + "' contains '" + spec.split(':')[0]
                + "', which violates this rule.")
        try:
            e = int(spec.split(':')[1])
        except:
            raise Exception(
                "When specifying column numbers, they must be integers: '" 
                + spec + "' contains '" + spec.split(':')[1] 
                + "', which violates this rule.")

        return line[b:e]
    else:
        try:
            c = int(spec) - 1
        except:
            raise Exception(
                "When specifying column numbers, they must be integers: '" 
                + spec + "' violates this rule.")

        try:
            line[c]
        except IndexError:
            raise Exception(
                "You specified a column number that doesn't exist: "
                + str(c + 1) + " (out of range 0 - " + str(len(line)) + ")")

        return [line[c]]

def match_line_and(line, match_list):
    '''
    Returns True if all match criteria matched

    Accepts:
        line: a list
        match_list: a string of , separated column:value pairs to match on

    Returns: True or False
    '''
    matches = listify(match_list)
    matched = False
    for match in matches:
        if ":" in match:
            try:
                c = int(match.split(':')[0]) - 1
            except:
                raise Exception(
                    "When specifying column numbers, they must be integers: '"
                    + match + "' contains '" + match.split(":")[0] + 
                    "', which violates this rule.")
            s = match.split(':')[1]
            try:
                if line[c] == s:
                    matched = True
                else:
                    matched = False
                    break
            except IndexError:
                raise Exception(
                    "You specified a column number that doesn't exist: " 
                    + str(c + 1))
        else:
            if match in line:
                matched = True
            else:
                matched = False
                break
    return matched

def match_line_or(line, match_list):
    '''
    Returns True if any match criteria matched

    Accepts:
        line: a list
        match_list: a string of , separated column:value pairs to attempt to match on

    Returns: True or False
    '''
    matches = listify(match_list)
    matched = False
    for match in matches:
        if ":" in match:
            try:
                c = int(match.split(':')[0]) - 1
            except:
                raise Exception(
                    "When specifying column numbers, they must be integers: '"
                    + match + "' contains '" + match.split(":")[0] + 
                    "', which violates this rule.")
            s = match.split(':')[1]
            try:
                if line[c] == s:
                    matched = True
                    break
            except IndexError:
                raise Exception(
                    "You specified a column number that doesn't exist: " 
                    + str(c + 1))
        else:
            if match in line:
                matched = True
                break
    return matched

def extracted_line(line, cl, delimiter):
    '''
    Return the string we will write to file, derived from the specified 
    columns of the supplied line.

    Accepts:
        line: a list
        cl: a string containing a delimited list of desired columns
        delimiter: delimiter to split line on

    Returns: a string
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
    parser.add_option("-d", "--delimiter", dest="delimiter", default="\t", 
        help="alternate delimiter (must be a single character.  DEFAULT is a TAB.)")
    parser.add_option("-i", "--infile", dest="inputfile", help="input file name")
    parser.add_option("-o", "--outfile", dest="outputfile", help="output file name")
    parser.add_option("-c", "--columns", dest="columns", 
        help="column numbers to select.  If not specified, all columns will be selected.  "
        "EX: 1:6 to select the first 6 columns, or 2:8,15 to select columns 2 - 8 and 15.  "
        "You can also say 1:3,9,4:7 to reorder columns in the output file.")
    parser.add_option("-n", "--column-names", dest="columns_by_name", 
        help="columns to select by column header name instead of column number.  "
        "This requires that the first line in the file be column headers.  "
        "Columns in the output file will apear in the order listed here.")
    parser.add_option("-m", "--match", dest="match", 
        help="(optional) column and string to match on.  EX: 2:chr1 to match "
        "all lines where column 2 contains 'chr1', or 'chr1' to match any column "
        "containing 'chr1'.  "
        "NOTE: multiple values listed together are ANDed together unless "
        "--match-mode is used also")
    parser.add_option("-r", "--match-or", action="store_true", dest="mode",
        help="Changes matching to OR mode instead of default AND mode")
    (options, args) = parser.parse_args()
    
    if not options.inputfile:
        parser.error('Input filename not given')

    if not options.outputfile:
        parser.error('Output filename not given')

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
                    if options.mode:
                        if match_line_or(line, options.match):
                            outfile.write(extracted_line(line, options.columns, options.delimiter))
                    else:    
                        if match_line_and(line, options.match):
                            outfile.write(extracted_line(line, options.columns, options.delimiter))
                # If we didn't specify a match criteria, write specified columns for all lines
                elif not options.match:
                    outfile.write(extracted_line(line, options.columns, options.delimiter))
            outfile.close()
        infile.close()