#!/usr/bin/env python

import argparse

from dwca import DwCAReader
from dwca.darwincore.utils import qualname as qn

from cartodb import CartoDBAPIKey, CartoDBException

# TODO: Better CLI Help
parser = argparse.ArgumentParser(description="Import a DarwinCore Archive file into CartDB.")

parser.add_argument('--domain', help='CartoDB domain.', required=True)
parser.add_argument('--api-key', dest='apikey', help='CartoDB user API key.', required=True)
parser.add_argument('--table', help="CartoDB table", required=True)
parser.add_argument('source_file', help="Source DwC-A file", type=argparse.FileType('r'))

args = parser.parse_args()

cl = CartoDBAPIKey(args.apikey, args.domain)

with DwCAReader(args.source_file) as dwca:
    # TODO: test type is occurrence, mandatory fields presents, ...
    sql = 'INSERT INTO {table} ({column_names}) VALUES ({column_values})'

    for line in dwca.each_line():
        lat = line.data[qn('decimalLatitude')]
        lon = line.data[qn('decimalLongitude')]

        formatted_sql = sql.format(table=args.table, 
                               column_names='the_geom',
                               column_values='ST_SetSRID(ST_Point(' + lon + ', ' + lat + '), 4326)')

        try:
            print cl.sql(formatted_sql)
        except CartoDBException as e:
            print ("CartDB error: ", e)