import requests

data_xml = requests.get(
    f"https://overpass-api.de/api/interpreter?"
    f'data=way["addr:city"="Екатеринбург"]'
    f'["addr:street"~"(улица Тургенева)'
    f'|(Тургенева улица)"]'
    f'["addr:housenumber"="4"];'
    f"out;"
).text

empty_data_xml = requests.get(
    f"https://overpass-api.de/api/interpreter?"
    f'data=way["addr:city"="Екатеринбург"]'
    f'["addr:street"~"(улица Ленина)|(Ленина улица)"]'
    f'["addr:housenumber" = "8"];'
    f"out;"
).text

data_node_xml = requests.get(
    f"https://overpass-api.de/api/interpreter?"
    f"data=node(498282056);" f"out;"
).text
