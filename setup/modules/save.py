import json

class saver:
    def __init__(self, setup_file='./data/setup_file.json', devices_file='./data/devices.json') -> None:
        self.setup_file = setup_file
        self.devices_file = devices_file

    def save_setup(self, interface, deamon=False, delay=5, device_location="./devices.json", backup_location="./backup.json"):
        setup = {
            "interface": interface.get_json(),

            "devices_list_location": device_location,
            "backup_location": backup_location,

            "deamon_active": deamon,
            "save_delay": delay
        }
        with open(self.setup_file, 'w') as f:
            json.dump(setup, f, indent=4)

    def save_devices(self, devices: list):
        devices = [device.get_info() for device in devices]
        with open(self.devices_file, 'w') as f:
            json.dump(devices, f, indent=4)