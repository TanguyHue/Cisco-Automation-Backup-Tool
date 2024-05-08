import json
from setup.modules.device import device as device_type

class saver:
    def __init__(self, setup_file='./data/setup_file.json', devices_file='./data/devices.json') -> None:
        self.setup_file = setup_file
        self.devices_file = devices_file

    def save_setup(self, interface, deamon, delay=5, 
                   device_location="./data/devices.json", backup_location="./data/backup"):
        setup = {
            "interface": interface.get_json(),

            "devices_list_location": device_location,
            "backup_location": backup_location,

            "deamon": deamon,
            "save_delay": delay
        }
        
        with open(self.setup_file, 'w') as f:
            json.dump(setup, f, indent=4)

    def save_devices(self, devices: list):
        devices = [device.get_info() for device in devices]
        with open(self.devices_file, 'w') as f:
            json.dump(devices, f, indent=4)

    def is_configured(self):
        try:
            with open(self.setup_file, 'r') as f:
                return True
        except FileNotFoundError:
            return False
        
def set_save(backup_location, devices_file):
    mac_address = backup_location.split('/')[-2].replace("-", ":")
    devices_list = json.load(open(devices_file, "r"))
    
    for device in devices_list:
        if device['mac'] == mac_address:
            device_info = device

    device = {
        'device_type': device_info["type"],
        'ip': device_info["ip"],
        'username': device_info["username"], 
        'password': device_info["password"], 
        'secret': device_info["enable_password"]
    }

    try:
        with open(backup_location, 'r') as f:
            #net_connect = netmiko.ConnectHandler(**device)
            #net_connect.enable()
            #for command in f:
            #    output = net_connect.send_config_set(command)
            #    print(output)
            #net_connect.disconnect()
            print(f"Configuration of {device_info['mac']} done")
    except FileExistsError:
        print("File not found")