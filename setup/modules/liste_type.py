import json
from setup.modules.type import type


class deviceType:
    def __init__(self) -> None:
        self.type_available = []
        types_availables = json.load(open("./data/type_available.json"))
        for item in types_availables:
            self.type_available.append(type(item['name'], item['value']))