import json

class saver:
    def __init__(self, setup_file='../../setup_file.json', devices_file='../../data/devices.json') -> None:
        self.setup_file = setup_file
        self.devices_file = devices_file

    def save_setup(self, setup):
        with open(self.setup_file, 'w') as f:
            json.dump(setup, f, indent=4)

    def save_devices(self, devices):
        with open(self.devices_file, 'w') as f:
            json.dump(devices, f, indent=4)