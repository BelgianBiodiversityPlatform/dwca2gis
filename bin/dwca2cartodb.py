#!/usr/bin/env python

import argparse
from cartodb import CartoDBAPIKey, CartoDBException

# TODO: Better CLI Help
parser = argparse.ArgumentParser(description="Import a DarwinCore Archive file into CartDB.")

parser.add_argument('--domain', help='CartoDB domain.', required=True)
parser.add_argument('--api-key', dest='apikey', help='CartoDB user API key.', required=True)
parser.add_argument('--table', help="CartoDB table", required=True)

args = parser.parse_args()

cl = CartoDBAPIKey(args.apikey, args.domain)
try:
    sql = 'INSERT INTO {table} ({column_names}) VALUES ({column_values})'
    formatted_sql = sql.format(table=args.table, 
                               column_names='the_geom',
                               column_values='ST_SetSRID(ST_Point(-110, 43),4326)')

    print cl.sql(formatted_sql)

except CartoDBException as e:
    print ("CartDB error: ", e)
