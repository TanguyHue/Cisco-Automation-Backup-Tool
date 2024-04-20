class device:
    def __init__(self, ip, mac) -> None:
        self.ip = ip
        self.mac = mac

    def get_text(self):
        return f"{self.ip} ({self.mac})"
    
    def get_info(self):
        return {
            "ip": self.ip,
            "mac": self.mac
        }