import unittest
import os
import tempfile
from argparse import Namespace
from shutil import rmtree

from ..dwca2shp import main

SAMPLE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'sample_files')
DWCA_SIMPLE_GIS_PATH = os.path.join(SAMPLE_DIR, 'dwca-simple_gis.zip')


class TestD2Shp(unittest.TestCase):
    def test_ioerror_inexistent_source(self):
        """Test an IOError is thrown when rying to open un inexistent DwC-A."""
        args = Namespace()
        args.source_file = "/i/dont/exist.zip"

        with self.assertRaises(IOError):
            main(args)

    def test_shapefile_created(self):
        """Ensure a Shapefile is created if called with correct parameters."""
        with destination_shapefile() as dest:
            args = Namespace()
            args.source_file = DWCA_SIMPLE_GIS_PATH
            args.destination = dest
            args.crs = 'epsg:4326'

            main(args)

            shapefile_dir_content = os.listdir(dest)
            self.assertIn('shapefile_out.shp', shapefile_dir_content)
            self.assertIn('shapefile_out.dbf', shapefile_dir_content)
            self.assertIn('shapefile_out.shx', shapefile_dir_content)

            # TODO: specific test for prj file ?
            self.assertIn('shapefile_out.prj', shapefile_dir_content)

    def test_default_crs(self):
        pass

    # TODO:
    # - Test absolute and relative path can be passed to command line
    # - Test a directory is created to hold the new shapefile
    # - Test number of produced lines
    # - Test prj file content
    # - Test when unknown CRS is asked
    # ...


class destination_shapefile:
    """ Returns a write path where a shapefile can be created.

        Returns the full path to a shepefile_out (non-existent) temporary,
        writable directory and ensure it is properly removed no matter what
        when leaving the 'with' block.

        Example:
            with destination_shapefile() as dest:
                create_shapefile(path=dest)

    """

    def __enter__(self):
        self.out_path = os.path.join(tempfile.gettempdir(), 'shapefile_out')
        return self.out_path

    def __exit__(self, type, value, traceback):
        rmtree(self.out_path, ignore_errors=True)
