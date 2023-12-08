import unittest
from unittest.mock import MagicMock, patch
from query_runner import QueryRunner


class TestQueryRunner(unittest.TestCase):
    def setUp(self):
        self.runner = QueryRunner()
        self.runner.cursor = MagicMock()
        self.runner.con = MagicMock()

    def test_create_table(self):
        self.runner._create_table()
        self.runner.cursor.execute.assert_called_once_with(
            """create table if not exists cities(
                                name text,
                                street text,
                                housenumber text,
                                postcode text,
                                lat text,
                                lon text,
                                name_organization text)"""
        )
        self.runner.con.commit.assert_called_once()

    @patch("sqlite3.connect")
    def test_enter(self, mock_connect):
        result = self.runner.__enter__()
        mock_connect.assert_called_once_with("cities.db")
        self.assertEqual(self.runner.con, mock_connect.return_value)
        self.assertEqual(
            self.runner.cursor,
            mock_connect.return_value.cursor.return_value)
        self.assertEqual(result, self.runner)

    def test_exit(self):
        self.runner.__exit__(None, None, None)
        self.runner.cursor.close.assert_called_once()
        self.runner.con.close.assert_called_once()

    def test_get_full_data_address(self):
        self.runner.get_full_data_address("City", "Street", "123")
        self.runner.cursor.execute.assert_called_once_with(
            """select * from cities
                                    where name='City'
                                    and (street='улица Street'
                                    or street='проспект Street')
                                    and housenumber='123';"""
        )
        self.runner.cursor.fetchall.assert_called_once()

    def test_write_full_data_address_without_name(self):
        data = {
            "addr:city": "City",
            "addr:street": "Street",
            "addr:housenumber": "123",
            "addr:postcode": "12345",
            "lat": "0.0",
            "lon": "0.0"
        }
        self.runner.write_full_data_address(data)
        self.runner.cursor.execute.assert_called_once_with(
            """insert or ignore into cities
            (name, street, housenumber, postcode, lat, lon, name_organization)
            values(?, ?, ?, ?, ?, ?, ?);
            """,
            (
                "City",
                "Street",
                "123",
                "12345",
                "0.0",
                "0.0",
                ""
            ),
        )
        self.runner.con.commit.assert_called_once()

    def test_write_full_data_address_with_name(self):
        data = {
            "addr:city": "City",
            "addr:street": "Street",
            "addr:housenumber": "123",
            "addr:postcode": "12345",
            "lat": "0.0",
            "lon": "0.0",
            "name": "Organization Name"
        }
        self.runner.write_full_data_address(data)
        self.runner.cursor.execute.assert_called_once_with(
            """insert or ignore into cities
            (name, street, housenumber, postcode, lat, lon, name_organization)
            values(?, ?, ?, ?, ?, ?, ?);
            """,
            (
                "City",
                "Street",
                "123",
                "12345",
                "0.0",
                "0.0",
                "Organization Name"
            ),
        )
        self.runner.con.commit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
