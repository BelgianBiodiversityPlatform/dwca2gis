import shapefile
import os

class ShapefileOutput:
    def __init__(self, filename):
        self.filename = filename

        self.w = shapefile.Writer(shapefile.POINT)
        self.w.field('myfield')
        self.w.autoBalance = 1

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        directory_name = self.filename

        os.mkdir(directory_name)
        self.w.save(os.path.join(directory_name, self.filename))

    def insert_line(self, lat, lon):
        try:
            lo = float(lon)
            la = float(lat)

            self.w.point(lo, la)
            self.w.record('toto')
        except ValueError:
            # Ruturn some-thing to display a warning to user
            pass