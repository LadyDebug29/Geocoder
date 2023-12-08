import unittest
from unittest.mock import patch
from http_handler import HTTPHandler


class TestHTTPHandler(unittest.TestCase):
    def setUp(self):
        self.handler = HTTPHandler()

    def test_handle_get_request(self):
        request = ("GET", "City,Street,1234")
        self.handler.handle(request, "нет")
        self.assertEqual(
            "City Street 1234",
            self.handler.get_standart_data())

    @patch("query_runner.QueryRunner.write_full_data_address")
    @patch("utils.write_to_json")
    def test_handle_post_request(
            self,
            mock_write_to_json, mock_write_full_data_address):
        request = (
            "POST",
            "addr:city=City,"
            "addr:street=Street,"
            "addr:housenumber=1234"
        )
        self.handler.handle(request, "да")
        self.assertTrue(mock_write_to_json.called)
        self.assertTrue(mock_write_full_data_address.called)

    def test_format_data_for_db(self):
        data_for_db = \
            (
                "addr_city:City,"
                "addr_street:Street,"
                "addr_housenumber:1234"
            )
        result = self.handler.format_data_for_db(data_for_db)
        expected = {
            "addr:city": "City",
            "addr:street": "Street",
            "addr:housenumber": "1234",
            "addr:postcode": "",
            "lat": "",
            "lon": "",
            "name": ""
        }
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
