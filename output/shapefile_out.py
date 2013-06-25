import os

import shapefile
import pyproj
import osr

EPSG_4326 = pyproj.Proj("+init=epsg:4326")


class ShapefileOutput:
    def __init__(self, filename, out_crs):
        self.filename = filename

        self.out_proj = pyproj.Proj("+init=" + out_crs)

        self.w = shapefile.Writer(shapefile.POINT)
        self.w.field('myfield')
        self.w.autoBalance = 1

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        directory_name = self.filename

        os.mkdir(directory_name)
        self.w.save(os.path.join(directory_name, self.filename))

        # We also create a .prj file with CRS metadata:
        prj = open(os.path.join(directory_name, (self.filename + '.prj')), "w")

        prj.write(self._proj4_to_wkt(self.out_proj.srs))
        prj.close()

    def insert_line(self, lat, lon):
        """ Insert a line in the shapefile. Lat/Lon are in EPSG:4326. """
        try:
            t = pyproj.transform(EPSG_4326, self.out_proj,
                                 float(lon), float(lat))
            self.w.point(t[0], t[1])
            self.w.record('toto')
        except ValueError:
            # Return some-thing to display a warning to user
            pass

    def _proj4_to_wkt(self, proj4):
        srs = osr.SpatialReference()
        srs.ImportFromProj4(proj4)
        return srs.ExportToWkt()
