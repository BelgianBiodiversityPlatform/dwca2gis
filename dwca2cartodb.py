#!/usr/bin/env python
import argparse
import sys

from dwca import DwCAReader
from dwca.darwincore.utils import qualname as qn
from cartodb import CartoDBAPIKey, CartoDBException

from utils import query_yes_no

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

    cl = CartoDBAPIKey(args.apikey, args.domain)

    if args.truncate:
        if query_yes_no("Are you sure you want to truncate the database ? Data will be LOST !", default="no"):
            cl.sql("TRUNCATE TABLE {table}".format(table=target_table))

    with DwCAReader(args.source_file) as dwca:

        # TODO: test type is occurrence, mandatory fields presents, ...
        sql = 'INSERT INTO {table} ({column_names}) VALUES ({column_values})'

        for line in dwca.each_line():
            lat = line.data[qn('decimalLatitude')]
            lon = line.data[qn('decimalLongitude')]

            formatted_sql = sql.format(table=target_table,
                                   column_names='the_geom',
                                   column_values='ST_SetSRID(ST_Point(' + lon + ', ' + lat + '), 4326)')

            try:
                cl.sql(formatted_sql)
                sys.stdout.write('.')
            except CartoDBException as e:
                print ("CartoDB error: ", e)


if __name__ == "__main__":
    main()
