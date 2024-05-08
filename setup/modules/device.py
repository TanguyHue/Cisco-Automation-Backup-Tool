import json


class device:
    def __init__(self, ip, mac, type = None, username = None, password = None, enable_password = None) -> None:
        self.ip = ip
        self.mac = mac
        self.type = type
        self.username = username
        self.password = password
        self.enable_password = enable_password

    def get_text(self):
        return f"{self.ip} ({self.mac})"
    
    def get_info(self):
        return {
            "ip": self.ip,
            "mac": self.mac
        }
    
    def get_full_info(self):
        return {
            "ip": self.ip,
            "mac": self.mac,
            "type": self.type,
            "username": self.username,
            "password": self.password,
            "enable_password": self.enable_password
        }
    
    def get_type(self):
        return self.type
    
    def get_type_name(self):
        types = json.load(open("./data/type_available.json", "r"))
        for type in types:
            if type['value'] == self.type:
                return type['name']
    
    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password

    def get_enable_password(self):
        return self.enable_password
    
    def get_ip(self):
        return self.ip

    def get_mac(self):
        return self.mac

    def set_info(self, type, username, password, enable_password):
        self.type = type
        self.username = username
        self.password = password
        self.enable_password = enable_password
        