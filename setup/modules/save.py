import json
import os

class saver:
    def __init__(self, devices_file='./data/devices.json') -> None:
        self.setup_file = './data/setup_file.json'
        self.devices_file = devices_file

    def save_setup(self, interface, daemon, delay_hour, delay_minute, 
                   device_location, backup_location, crontab_location):
        self.devices_file = device_location
        setup = {
            "interface": interface.get_json(),

            "devices_list_location": device_location,
            "backup_location": backup_location,
            "crontab_location": crontab_location,

            "daemon": daemon,
            "delay_hour": delay_hour,
            "delay_minute": delay_minute
        }
        
        if not os.path.exists(os.path.dirname(self.setup_file)):
            os.makedirs(os.path.dirname(self.setup_file))
            with open(os.path.dirname(self.setup_file) + 'type_available.json', 'w') as f:
                json.dump([
                    {
                        "name": "Cisco IOS",
                        "value": "cisco_ios"
                    },
                    {
                        "name": "Other",
                        "value": "other"
                    },], f, indent=4)
        with open(self.setup_file, 'w') as f:
            json.dump(setup, f, indent=4)

    def save_devices(self, devices: list):
        devices = [device.get_info() for device in devices]
        if not os.path.exists(os.path.dirname(self.devices_file)):
            os.makedirs(os.path.dirname(self.devices_file))
            with open(os.path.dirname(self.devices_file) + 'type_available.json', 'w') as f:
                json.dump([
                    {
                        "name": "Cisco IOS",
                        "value": "cisco_ios"
                    },
                    {
                        "name": "Other",
                        "value": "other"
                    },], f, indent=4)
        with open(self.devices_file, 'w') as f:
            json.dump(devices, f, indent=4)

    def is_configured(self):
        try:
            with open(self.setup_file, 'r') as f:
                return True
        except FileNotFoundError:
            return False