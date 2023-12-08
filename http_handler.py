from query_runner import QueryRunner
import utils


class HTTPHandler:
    forms_get_query = {"GET", "Get", "get"}
    forms_post_query = {"POST", "Post", "post"}

    def __init__(self):
        self.__standart_data = ""
        self.is_get_query_processed = False

    def handle(self, request, save_to_json):
        method, data = request
        for option in self.forms_get_query:
            if method == option:
                self.__handle_get_request(data)
                self.is_get_query_processed = True
                return
        for option in self.forms_post_query:
            if method == option:
                self.__handle_post_request(data, save_to_json)
                return

    def __handle_get_request(self, request):
        self.__standart_data = (
            request.split("/")[-1].replace(",", " ").replace("_", " ")
        )

    def __handle_post_request(self, request, save_json_flag):
        data_for_db = request.split("/")[-1]
        format_data = self.format_data_for_db(data_for_db)
        with QueryRunner() as query_runner:
            query_runner.write_full_data_address(format_data)
        if save_json_flag == "да":
            data_for_json = []
            for elem in format_data:
                data_for_json.append(format_data[elem])
            utils.write_to_json(data_for_json)

    @staticmethod
    def format_data_for_db(data_for_db):
        tags = {
            "addr:city": "",
            "addr:street": "",
            "addr:housenumber": "",
            "addr:postcode": "",
            "lat": "",
            "lon": "",
            "name": "",
        }
        for elem in data_for_db.split(","):
            tag, data = elem.split(":")
            tags[tag.replace("_", ":")] = data
        return tags

    def get_standart_data(self):
        return self.__standart_data
