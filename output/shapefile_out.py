import os

import shapefile
import pyproj
import osr

EPSG_4326 = pyproj.Proj("+init=epsg:4326")


class ShapefileOutput:
    def __init__(self, path, out_crs, additional_fields_names):
        self.path = path
        self.additional_fields_names = additional_fields_names

        self.out_proj = pyproj.Proj("+init=" + out_crs)

        self.w = shapefile.Writer(shapefile.POINT)

        for f in additional_fields_names:
            self.w.field(str(f))

        self.w.autoBalance = 1

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        directory_name = self.path
        filename = os.path.basename(directory_name)

        # Put the whole shapefile in its own directory (same name than .shp file)
        os.mkdir(directory_name)
        self.w.save(os.path.join(directory_name, filename))

        # We also create a .prj file with CRS metadata:
        prj = open(os.path.join(directory_name, (filename + '.prj')), "w")

        prj.write(self._proj4_to_wkt(self.out_proj.srs))
        prj.close()

    def insert_line(self, lat, lon, additional_fields_content):
        # additional_fields_content are expected in the same order than in __init__

        """ Insert a line in the shapefile. Lat/Lon are in EPSG:4326. """
        try:
            t = pyproj.transform(EPSG_4326, self.out_proj,
                                 float(lon), float(lat))
            self.w.point(t[0], t[1])
        except ValueError:
            # TODO: Return something to display a warning to user
            pass

        self.w.record(*additional_fields_content)

    def _proj4_to_wkt(self, proj4):
        srs = osr.SpatialReference()
        srs.ImportFromProj4(proj4)
        return srs.ExportToWkt()
