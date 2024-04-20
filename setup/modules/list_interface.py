import netifaces
from setup.modules.interface import interface

class interfaces:
    def __init__(self): 
        self.interfaces = netifaces.interfaces()
        self.interface_address = []

        for interface_name in self.interfaces:
            ipv4_info = netifaces.ifaddresses(interface_name).get(netifaces.AF_INET)
            if ipv4_info:
                ipv4_address = ipv4_info[0]['addr']
                netmask = ipv4_info[0]['netmask']
                if ipv4_info[0].get('broadcast') is not None:
                    self.interface_address.append(
                        interface(interface_name, ipv4_address, netmask))
    
    def get_interface(self, interface_name):
        for interface in self.interface_address:
            if ("['" + interface['interface'] + "']") == interface_name:
                return interface
        return None

    def get_address_mask(self, interface):
        return f"{interface['ipv4_address']}/{netifaces.ifaddresses(interface['interface'])[netifaces.AF_INET][0]['netmask']}"
