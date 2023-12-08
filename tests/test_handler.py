import unittest
import tests.test_data_xml as test_data_xml
from parser_xml import Parser


class HandlerTest(unittest.TestCase):
    def setUp(self):
        self.parser = Parser(test_data_xml.data_xml, "test_data.xml")
        self.parser_empty_data = Parser(
            test_data_xml.empty_data_xml, "test_empty_data.xml"
        )
        self.parser_node = Parser(
            test_data_xml.data_node_xml, "test_data_node.xml"
        )

    def test_parse_point_identifier(self):
        point_identifier = self.parser.parse_point_identifier("test_data.xml")
        self.assertEqual(point_identifier, "498282056")

    def test_parse_point_identifier_in_empty_file(self):
        point_identifier = self.parser_empty_data.parse_point_identifier(
            "test_empty_data.xml"
        )
        self.assertEqual(point_identifier, "")

    def test_parse_received_data(self):
        received_data = self.parser.parse_received_data("test_data.xml")
        correct_result = {
            "addr:city": "Екатеринбург",
            "addr:country": "RU",
            "addr:housenumber": "4",
            "addr:postcode": "620083",
            "addr:street": "улица Тургенева",
            "building": "university",
            "building:levels": "7",
        }
        self.assertSequenceEqual(received_data, correct_result)

    def test_parse_lat_and_lon(self):
        lat, lon = self.parser_node.parse_lat_and_lon("test_data_node.xml")
        self.assertSequenceEqual((lat, lon), ("56.8405741", "60.6152215"))


if __name__ == "__main__":
    unittest.main()
