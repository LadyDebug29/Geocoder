class RequestHandler:
    city_prefix_options = {
        "г",
        "Г",
        "город",
        "Город",
        "гор",
        "Гор",
        "г.",
        "Г.",
        "гор.",
        "Гор.",
    }
    street_prefix_options = {
        "у",
        "У",
        "ул",
        "Ул",
        "улица",
        "Улица",
        "у.",
        "У.",
        "ул.",
        "Ул.",
    }
    types_streets_included_in_address_name = {"проспект"}

    def __init__(self):
        self.city = ""
        self.street = ""
        self.house_number = ""

    def handle(self, address):
        split_address_words = address.split()
        split_address_words_without_prefix = []
        for word in split_address_words:
            if (
                word not in self.city_prefix_options
                and word not in self.street_prefix_options
                and word not in self.types_streets_included_in_address_name
            ):
                split_address_words_without_prefix.append(word)

        self.city = (
            split_address_words_without_prefix[0][0].upper()
            + split_address_words_without_prefix[0][1:]
        )
        i = 1
        while i != len(split_address_words_without_prefix) - 1:
            self.street += split_address_words_without_prefix[i] + " "
            i += 1
        self.street = self.street[0].upper() + self.street[1:]
        self.street = self.street.strip()
        house_number = split_address_words_without_prefix[-1]
        if house_number[-1].isalpha():
            self.house_number = (
                house_number[: len(house_number) - 1] +
                house_number[-1].upper()
            )
        else:
            self.house_number = house_number
