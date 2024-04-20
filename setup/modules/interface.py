import ipaddress


class interface:
    def __init__(self, interface_name, ipv4_address, netmask) -> None:
        self.interface_name = interface_name
        self.ipv4_address = ipv4_address
        self.netmask = netmask

    def get_cidr(self):
        return ipaddress.IPv4Network(f"{self.ipv4_address}/{self.netmask}", 
                                     strict=False).prefixlen
    
    def get_name(self):
        return self.interface_name
    
    def get_network_address(self):
        return ipaddress.IPv4Network(f"{self.ipv4_address}/{self.netmask}", 
                                     strict=False).network_address
    
    def get_text(self):
        return f"{self.interface_name}: Network {self.get_network_address()} | IP Address {self.ipv4_address} | Broadcast {self.broadcast}"
    
    def get_address(self):
        return self.ipv4_address
    
    def get_json(self):
        return {
            "interface": self.interface_name,
            "ipv4_address": self.ipv4_address,
            "netmask": self.netmask
        }