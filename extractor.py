#!/usr/bin/env python

import csv, sys
from optparse import OptionParser
csv.field_size_limit(sys.maxsize)

def writeln(line, f):
    '''Always grab the first six columns'''
    f.write("\t".join(line[0:6]))
    f.write("\n")

if __name__ == '__main__':

    '''
    A simple utility that grabs the first 6 columns of a TSV file.  If you 
    specify a chromosome number, only lines that match that chromosome number
    in the second column will be written to the output file.  This, of course,
    assumes that the second column follows the pattern "chr#".  Assumptions
    have been made.
    '''

    parser = OptionParser()
    parser.add_option("-i", "--infile", dest="inputfile", help="input FILE")
    parser.add_option("-o", "--outfile", dest="outputfile", help="output FILE")
    parser.add_option("-c", "--chromosome", dest="chromosome", 
        help="chromosome being selected from column 2.  If none is specified, all lines will be selected.")
    (options, args) = parser.parse_args()
    
    if not options.inputfile:
        parser.error('Input filename not given')

    if not options.outputfile:
        parser.error('Output filename not given')

    with open(options.inputfile, 'r') as infile:
        with open(options.outputfile, 'w') as outfile:
            i = 0
            for line in csv.reader(infile, delimiter='\t', quoting=csv.QUOTE_NONE ):
                # Always write the first line of the file (column names)
                if i == 0:
                    writeln(line, outfile)
                    i += 1
                # If we specified a chromosome, only write lines that pertain to that one
                elif options.chromosome and line[1]  == 'chr' + options.chromosome:
                    writeln(line, outfile)
                # If we didn't specify a chromosome, write all lines
                elif not options.chromosome:
                    writeln(line, outfile)
            outfile.close()
        infile.close()