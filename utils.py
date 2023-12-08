import json


def write_to_json(data):
    with open("osm_data.json", "r") as json_file:
        json_data = json.load(json_file)
        json_data[f"{data[0]} {data[1]} {data[2]}"] = data
    with open("osm_data.json", "w") as json_file:
        json.dump(json_data, json_file, indent=4)
