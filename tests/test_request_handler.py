import unittest
import request_handler


class RequestHandlerTest(unittest.TestCase):
    def setUp(self):
        self.request_handler = request_handler.RequestHandler()

    def tests_handle(self):
        for city_prefix in self.request_handler.city_prefix_options:
            for street_prefix in self.request_handler.street_prefix_options:
                for register_city_name in "еЕ":
                    for register_street_name in "тТ":
                        self.request_handler.city = ''
                        self.request_handler.street = ''
                        self.request_handler.house_number = ''
                        address = (
                            city_prefix
                            + f" {register_city_name}катеринбург "
                            + street_prefix
                            + f" {register_street_name}ургенева 4"
                        )
                        self.request_handler.handle(address)
                        city, street, housenumber = (
                            self.request_handler.city,
                            self.request_handler.street,
                            self.request_handler.house_number,
                        )
                        self.assertSequenceEqual(
                            (city, street, housenumber),
                            ("Екатеринбург", "Тургенева", "4"),
                        )


if __name__ == "__main__":
    unittest.main()
