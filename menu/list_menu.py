import json

class item_menu:
    def __init__(self, name, value) -> None:
        self.titre = name
        self.value = value

    def get_text(self):
        return self.titre
    
    def get_value(self):
        return self.value

class menu_list:
    def __init__(self) -> None:
        self.item_menu = []
        items = json.load(open("./menu/menu.json"))
        for item in items:
            self.item_menu.append(item_menu(item['titre'], item['value']))
        self.item_menu.append(item_menu("Quit", len(self.item_menu)))
    
    def length(self):
        return len(self.item_menu)