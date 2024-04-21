import json

class type:
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

    def get_text(self):
        return self.name
    
    def get_type(self):
        return self.value
class deviceType:
    def __init__(self) -> None:
        self.type_available = []
        types_availables = json.load(open("./data/type_available.json"))
        for item in types_availables:
            self.type_available.append(type(item['name'], item['value']))