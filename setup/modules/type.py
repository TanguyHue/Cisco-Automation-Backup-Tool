class type:
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

    def get_text(self):
        return self.name
    
    def get_type(self):
        return self.value