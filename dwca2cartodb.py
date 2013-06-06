#!/usr/bin/env python
import argparse
import sys

from cartodb import CartoDBException
from dwca import DwCAReader

from utils import query_yes_no, dwcaline_to_epsg4326, valid_dwca
from output.cartodb_out import CartoDBOutput

DEFAULT_IMPORTED_FIELDS = ['occurrenceID', 'scientificName', 'eventDate']

def main():
    # TODO: Better CLI Help
    parser = argparse.ArgumentParser(
        description="Import a DarwinCore Archive file into CartDB.")

    parser.add_argument('--domain',
                        help='Your CartoDB domain (without .cartodb.com).',
                        required=True)
    parser.add_argument('--api-key', 
                        dest='apikey',
                        help='Your CartoDB API key.',
                        required=True)
    parser.add_argument('--table',
                        help="CartoDB destination table name",
                        required=True)
    parser.add_argument('--truncate-table',
                        action='store_true',
                        dest='truncate',
                        help="Truncate destination table prior to import.")
    parser.add_argument('source_file',
                        help="Source DwC-A file", 
                        type=argparse.FileType('r'))

    args = parser.parse_args()

    target_table = args.table

    out = CartoDBOutput(args.apikey, args.domain, args.table)

    if args.truncate:
        if query_yes_no("Are you sure you want to truncate the database ? Data will be LOST !", default="no"):
            out.truncate_table()

    with DwCAReader(args.source_file) as dwca:
        if valid_dwca(dwca):    
            for line in dwca.each_line():
                try:
                    out.insert_line(**dwcaline_to_epsg4326(line))
                    sys.stdout.write('.')
                except CartoDBException as e:
                    print ("CartoDB error: ", e)
        else:
            # TODO: more detailed message
            print "Invalid source DwC-A file."

if __name__ == "__main__":
    main()
