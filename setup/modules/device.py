class device:
    def __init__(self, ip, mac) -> None:
        self.ip = ip
        self.mac = mac
        self.type = None
        self.username = None
        self.password = None

    def get_text(self):
        return f"{self.ip} ({self.mac})"
    
    def get_info(self):
        return {
            "ip": self.ip,
            "mac": self.mac
        }
    
    def get_ip(self):
        return self.ip

    def set_info(self, type, username, password):
        self.type = type
        self.username = username
        self.password = password
        