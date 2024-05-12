import os
from backup.modules.backup import backup
from menu.conf import list_device, conf_devices
from setup.modules.interface import interface
from setup.modules.save import saver
import json

def main():
    setup = json.load(open("./data/setup_file.json"))
    json_interface = setup['interface']
    interface_object = interface(json_interface['interface'], json_interface['ipv4_address'], json_interface['netmask'])
    backup_location = setup['backup_location']
    device_location = setup['devices_list_location']

    devices = list_device(interface_object)
    saver().save_devices(devices)
    conf_devices()

    backupFile = backup(backup_location, device_location)
    backupFile.reset()
    backupFile.save()

    print("Scan finished")
    input("Press enter to continue...")
    os.system("clear")