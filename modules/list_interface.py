import netifaces
import ipaddress

class interfaces:
    def __init__(self): 
        self.interfaces = netifaces.interfaces()
        self.interface_address = []

        for interface in self.interfaces:
            ipv4_info = netifaces.ifaddresses(interface).get(netifaces.AF_INET)
            if ipv4_info:
                ipv4_address = ipv4_info[0]['addr']
                netmask = ipv4_info[0]['netmask']
                if ipv4_info[0].get('broadcast') is not None:
                    broadcast = ipv4_info[0]['broadcast']
                    network_address = ipaddress.IPv4Network(f"{ipv4_address}/{netmask}", strict=False).network_address
                    text = f"{interface}: Network {network_address} | IP Address {ipv4_address} | Broadcast {broadcast}"
                    self.interface_address.append({
                        'interface': interface, 
                        'network_address': network_address, 
                        'ipv4_address': ipv4_address, 
                        'broadcast': broadcast,
                        'text': text,
                        })
