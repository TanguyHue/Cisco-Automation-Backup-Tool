import os
import json
import threading
import time

class backup:
    def __init__(self, location, devices_location) -> None:
        self.location =  location
        self.devices_location = devices_location

    def reset(self):
        os.system(f"rm -rf {self.location}")

    def save(self):
        devices = json.load(open(self.devices_location, 'r'))

        if not os.path.exists(self.location):
            os.makedirs(self.location, mode = 0o777, exist_ok=True)
        
        if not os.path.exists(f"{self.location}/.gitignore"):
            with open(f"{self.location}/.gitignore", 'w') as f:
                f.write("*\n!.gitignore\n")

        successful_devices = []

        for device in devices:
            name = device['mac'].replace(':', '-')
            print(f"Test of pinging {name} | {device['ip']}")
            self.ping_terminé = False
            def afficher_attente():
                while True and not self.ping_terminé:
                    for i in range(3):
                        print("Waiting ping response" + "." * (i + 1), end="\r")
                        time.sleep(0.4)
                        print("\033[K", end="")
            
            # Démarrer l'affichage en attente en arrière-plan
            thread = threading.Thread(target=afficher_attente)
            thread.daemon = True
            thread.start()
            os.makedirs(f"{self.location}/{name}", mode = 0o777, exist_ok=True)
            os.system(f"ping -c 3 {device['ip']} > {self.location}/{name}/ping.txt")

            with open(f"{self.location}/{name}/ping.txt", 'r') as f:
                if "100% packet loss" in f.read():
                    print("\033[K", end="")
                    print("Ping failed")
                    print("Device deleted")
                    os.system(f"rm -rf {self.location}/{name}")
                else:
                    print("\033[K", end="")
                    print("Ping success")
                    successful_devices.append(device)
            
            self.ping_terminé = True    # Arrêter l'affichage en attente
            thread.join()

        
        with open(self.devices_location, 'w') as f:
            json.dump(successful_devices, f, indent=4)