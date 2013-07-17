import unittest
from argparse import Namespace

from ..dwca2shp import main


class TestD2Shp(unittest.TestCase):
    def test_ioerror_inexistent_source(self):
        """ Test an IOError is thrown when asking to convert un inexistent DwC-A. """
        args = Namespace()
        args.source_file = "/i/dont/exist.zip"

        with self.assertRaises(IOError):
            main(args)
