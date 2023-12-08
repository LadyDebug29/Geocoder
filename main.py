import requests
import click
import parser_xml
import request_handler
from query_runner import QueryRunner
import utils
from http_handler import HTTPHandler


def start_handle_standart_data(address, save_json_flag):
    req_handler = request_handler.RequestHandler()
    req_handler.handle(address)
    with QueryRunner() as query_runner:
        full_data_address = query_runner.get_full_data_address(
            req_handler.city, req_handler.street, req_handler.house_number
        )
        if full_data_address:
            for elem in full_data_address[0]:
                print(elem)
        else:
            data_xml = requests.get(
                f"https://overpass-api.de/api/interpreter?"
                f'data=way["addr:city"="{req_handler.city}"]'
                f'["addr:street"~"(улица {req_handler.street})'
                f"|({req_handler.street} улица)"
                f"|({req_handler.street} проспект)"
                f'|(проспект {req_handler.street})"]'
                f'["addr:housenumber"="{req_handler.house_number}"];'
                f"out;"
            ).text
            parser = parser_xml.Parser(data_xml, "data.xml")
            point_identifier = parser.parse_point_identifier("data.xml")
            data = parser.parse_received_data("data.xml")
            if not data:
                print("Адрес не был найден")
            else:
                data_node_xml = requests.get(
                    f"https://overpass-api.de/api/interpreter?"
                    f"data=node({point_identifier});"
                    f"out;"
                ).text
                parser = parser_xml.Parser(data_node_xml, "data.xml")
                data["lat"], data["lon"] = parser.parse_lat_and_lon(
                    "data.xml"
                )
                query_runner.write_full_data_address(data)
                full_data_address = query_runner.get_full_data_address(
                    req_handler.city,
                    req_handler.street,
                    req_handler.house_number
                )
                if full_data_address:
                    if save_json_flag == "да":
                        utils.write_to_json(full_data_address[0])
                    for elem in full_data_address[0]:
                        if elem != "":
                            print(elem)


def get_description_command_http_request():
    return (
        "Позволяет отправить get- или post-запрос"
        "(про структуру запросов читайте в README"
    )


def get_description_command_save_to_json():
    return "Сохранить или нет полученные или отправленные данные в json"


@click.command()
@click.option(
    "--http-request",
    default=None,
    nargs=2,
    help=get_description_command_http_request()
)
@click.option(
    "--save-to-json",
    default="нет",
    type=click.STRING,
    help=get_description_command_save_to_json(),
)
@click.argument(
    "standart_input",
    default=None,
    nargs=-1,
    type=click.STRING)
def main(standart_input, http_request, save_to_json):
    """

    Args:
        save_to_json: сохранить в json или нет
        http_request: сделать http-запрос, как он указан в README.md
        standart_input: ввод данных в стандартном формате
        г Екатеринбург ул Тургенева 4

    Returns:
        Возможный вывод:
        Екатеринбург улица Тургенева 4 620083 56.8405741 60.6152215
    """
    if http_request:
        http_handler = HTTPHandler()
        http_handler.handle(http_request, save_to_json)
        if http_handler.is_get_query_processed:
            start_handle_standart_data(
                http_handler.get_standart_data(),
                save_to_json)

    elif standart_input:
        format_standart_input = " ".join(standart_input)
        start_handle_standart_data(format_standart_input, save_to_json)


if __name__ == "__main__":
    main()
