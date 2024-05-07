import os
from backup.modules.backup import backup
from menu.conf import list_device, conf_devices
from setup.modules.interface import interface
from setup.modules.save import saver
import json

def main():
    json_interface = json.load(open("./data/setup_file.json"))['interface']
    interface_object = interface(json_interface['interface'], json_interface['ipv4_address'], json_interface['netmask'])

    devices = list_device(interface_object)
    saver().save_devices(devices)
    conf_devices()

    backupFile = backup("./data/backup", "./data/devices.json")
    backupFile.reset()
    backupFile.save()

    print("Scan finished")
    input("Press enter to continue...")
    os.system("clear")