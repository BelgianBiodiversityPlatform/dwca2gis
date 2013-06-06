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