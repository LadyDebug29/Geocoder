from lxml import etree


class Parser:
    def __init__(self, data_xml, xml_file_for_processing):
        with open(
                f"{xml_file_for_processing}",
                "w",
                encoding="utf-8"
        ) as f:
            f.truncate(0)
            f.write(data_xml)

    @staticmethod
    def parse_point_identifier(xml_file_for_processing):
        point_identifier = ""
        with open(
                f"{xml_file_for_processing}",
                "r",
                encoding="utf-8"
        ) as f:
            tree = etree.parse(f)
            root = tree.getroot()
            for tag in root.iter("nd"):
                point_identifier = tag.get("ref")
        return point_identifier

    @staticmethod
    def parse_received_data(xml_file_for_processing):
        data = dict()
        with open(
                f"{xml_file_for_processing}",
                "r",
                encoding="utf-8"
        ) as f:
            tree = etree.parse(f)
            root = tree.getroot()
            for tag in root.iter("tag"):
                data[tag.get("k")] = tag.get("v")
        return data

    @staticmethod
    def parse_lat_and_lon(xml_file_for_processing):
        lat, lon = "", ""
        with open(
                f"{xml_file_for_processing}",
                "r",
                encoding="utf-8"
        ) as f:
            tree = etree.parse(f)
            root = tree.getroot()
            for tag in root.iter("node"):
                lat, lon = tag.get("lat"), tag.get("lon")
        return str(lat), str(lon)
