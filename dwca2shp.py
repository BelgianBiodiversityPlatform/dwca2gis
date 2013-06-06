#!/usr/bin/env python
import argparse
import sys

from dwca import DwCAReader

from output import ShapefileOutput
from utils import dwcaline_to_epsg4326, valid_dwca

DEFAULT_IMPORTED_FIELDS = ['occurrenceID', 'scientificName', 'eventDate']


def main():
    parser = argparse.ArgumentParser(
        description="Convert a DarwinCore Archive file to an ESRI Shapefile.")

    parser.add_argument('source_file',
                        help="Source DwC-A file", 
                        type=argparse.FileType('r'))

    parser.add_argument('destination',
                        help="Name of shapefile (directory) to be created")

    args = parser.parse_args()

    with DwCAReader(args.source_file) as dwca:
        if valid_dwca(dwca):
            with ShapefileOutput(args.destination) as out:
                for line in dwca.each_line():
                    out.insert_line(**dwcaline_to_epsg4326(line))
                    sys.stdout.write('.')


if __name__ == "__main__":
    main()
