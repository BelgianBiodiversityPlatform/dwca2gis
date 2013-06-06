import shapefile
from cartodb import CartoDBAPIKey

class CartoDBOutput:
    SQL = 'INSERT INTO {table} ({column_names}) VALUES ({column_values})'

    def __init__(self, apikey, domain, table):
        self.table = table
        self.cl = CartoDBAPIKey(apikey, domain)

    def insert_line(self, lat, lon):
        """ Insert a line in the configured CartoDB table. Lat/Lon are in EPSG:4326. """

        formatted_sql = self.SQL.format(table=self.table,
                                   column_names='the_geom',
                                   column_values='ST_SetSRID(ST_Point(' + lon + ', ' + lat + '), 4326)')

        self.cl.sql(formatted_sql)

    def truncate_table(self):
        self.cl.sql("TRUNCATE TABLE {table}".format(table=self.table))

class ShapefileOutput:
    def __init__(self, filename):
        self.filename = filename

        self.w = shapefile.Writer(shapefile.POINT)
        self.w.field('myfield')
        self.w.autoBalance = 1

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.w.save(self.filename)

    def insert_line(self, lat, lon):
        try:
            lo = float(lon)
            la = float(lat)

            self.w.point(lo, la)
            self.w.record('toto')
        except ValueError:
            # Ruturn some-thing to display a warning to user
            pass
        
        # print "lon: " + lon
        # self.w.point(lo, la)
        # #self.w.point(2,3)
        # print("pass2")