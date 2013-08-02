#!/usr/bin/env python
import argparse
import sys

from dwca import DwCAReader

from output.shapefile_out import ShapefileOutput
from utils import (dwcaline_to_epsg4326, valid_dwca, CannotConvertException,
                   unicode_to_ascii)

DEFAULT_IMPORTED_FIELDS = ['occurrenceID', 'scientificName', 'eventDate']


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert a DarwinCore Archive file to an ESRI Shapefile.")

    parser.add_argument('source_file',
                        help="Source DwC-A file",
                        type=argparse.FileType('r'))

    parser.add_argument('destination',
                        help="Name of shapefile (directory) to be created")

    parser.add_argument('--crs',
                        help="Output projection, default to epsg:4326",
                        default='epsg:4326')

    return parser.parse_args()


def main(args):
    with DwCAReader(args.source_file) as dwca:
        if valid_dwca(dwca):
            ordered_fields = list(dwca.core_terms)
            # Only last part as Shapefiles field names are limited to 10 chars
            ordered_fields_truncated = [f.rsplit('/')[-1] for f in ordered_fields]
            import pdb; pdb.set_trace()

            with ShapefileOutput(args.destination, args.crs, ordered_fields_truncated) as out:
                for line in dwca.each_line():
                    try:
                        gis_data = dwcaline_to_epsg4326(line)
                        additional_values = [unicode_to_ascii(line.data[f]) for f in ordered_fields]

                        out.insert_line(gis_data['lat'], gis_data['lon'], additional_values)
                        sys.stdout.write('.')
                    except CannotConvertException:
                        pass

if __name__ == "__main__":
    args = parse_args()
    main(args)
