import os
import json

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
            print(f"Test de ping à {name} | {device['ip']}")
            os.makedirs(f"{self.location}/{name}", mode = 0o777, exist_ok=True)
            os.system(f"ping -c 1 {device['ip']} > {self.location}/{name}/ping.txt")

            with open(f"{self.location}/{name}/ping.txt", 'r') as f:
                if "1 packets transmitted, 1 received" in f.read():
                    print("Ping réussi")
                    successful_devices.append(device)
                else:
                    print("Ping échoué")
                    print("Suppression de l'appareil")
                    os.system(f"rm -rf {self.location}/{name}")
        
        with open(self.devices_location, 'w') as f:
            json.dump(successful_devices, f, indent=4)