import sqlite3


class QueryRunner:
    def __init__(self):
        pass

    def __enter__(self):
        self.con = sqlite3.connect("cities.db")
        self.cursor = self.con.cursor()
        self._create_table()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.con.close()

    def _create_table(self):
        self.cursor.execute(
            """create table if not exists cities(
                                name text,
                                street text,
                                housenumber text,
                                postcode text,
                                lat text,
                                lon text,
                                name_organization text)"""
        )
        self.con.commit()

    def get_full_data_address(self, city, street, house_number):
        self.cursor.execute(
            f"""select * from cities
                                    where name='{city}'
                                    and (street='улица {street}'
                                    or street='проспект {street}')
                                    and housenumber='{house_number}';"""
        )
        full_address = self.cursor.fetchall()
        return full_address

    def write_full_data_address(self, data):
        if "name" not in data:
            data["name"] = ""
        self.cursor.execute(
            f"""insert or ignore into cities
            (name, street, housenumber, postcode, lat, lon, name_organization)
            values(?, ?, ?, ?, ?, ?, ?);
            """,
            (
                data["addr:city"]
                if "addr:city" in data.keys() else "",
                data["addr:street"]
                if "addr:street" in data.keys() else "",
                data["addr:housenumber"]
                if "addr:housenumber" in data.keys() else "",
                data["addr:postcode"]
                if "addr:postcode" in data.keys() else "",
                data["lat"]
                if "lat" in data.keys() else "",
                data["lon"]
                if "lon" in data.keys() else "",
                data["name"]
                if "name" or "brand" or "operator" in data.keys() else "",
            ),
        )
        self.con.commit()
