import os
import json

class backup:
    def __init__(self, location, devices_location) -> None:
        self.location =  location
        self.devices_location = devices_location

    def save(self):
        devices = json.load(open(self.devices_location, 'r'))

        if not os.path.exists(self.location):
            os.makedirs(self.location)

        for device in devices:
            name = device['mac'].replace(':', '-')
            print("Appareil:", name)
            os.system(f"ping -c 1 {device['ip']} > {self.location}/{name}.txt")