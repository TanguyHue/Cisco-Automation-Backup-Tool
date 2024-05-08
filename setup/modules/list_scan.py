import scapy.all as scapy
import time
import threading
import os
from setup.modules.device import device

class scanner:
    def __init__(self, ip = "192.168.8.175/24") -> None:
        self.ip = ip
        self.scan_terminé = False
        self.results = []

    def scan(self) -> list:
        os.system("clear")
        def afficher_attente():
            while True and not self.scan_terminé:
                for i in range(3):
                    print("Scan still running" + "." * (i + 1), end="\r")
                    time.sleep(0.4)
                    print("\033[K", end="")
        
        thread = threading.Thread(target=afficher_attente)
        thread.daemon = True
        thread.start()

        arp_request = scapy.ARP(pdst=self.ip)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

        for element in answered_list:
            self.results.append(device(element[1].psrc, element[1].hwsrc))
        
        self.scan_terminé = True 
        thread.join()
        return self.results
