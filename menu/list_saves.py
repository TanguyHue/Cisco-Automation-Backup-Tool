import json
import os
from time import strptime
from setup.modules.device import device as device_type
from setup.modules.list import listClass as list
from file_comparaison.modules.compare import compareClass
import curses

class option_type:
    def __init__(self, text) -> None:
        self.text = text

    def get_text(self):
        return self.text
    
class backup_type:
    def __init__(self, text, index, last_save = False) -> None:
        self.name = text
        if last_save:
            text += " (Last save)"
        self.text = text
        self.index = index

    def get_text(self):
        return self.text
    
    def get_name(self):
        return self.name
    
    def get_index(self):
        return self.index
    
    def last_save(self):
        self.text += " (Last save)"

def load_devices(path="./data/devices.json"):
    with open(path, "r") as file:
        devices_load = json.load(file)
    devices = []
    for device in devices_load:
        devices.append(device_type(device['ip'], device['mac'], device['type'], device['username'], device['password']))
    return devices

def device_list(devices):
    options = []
    options.append(option_type("Make a backup for all devices"))
    options.append(option_type("Quit"))
    liste = list(devices + options, 'Choose a devices', True, False)
    curses.wrapper(liste.executer)
    selected_device = [device for device, checked in zip(liste.items, liste.checked) if checked][0]
    return selected_device

def backup_list(device: device_type):   
    options = []
    options.append(option_type("Make a backup for this device"))
    options.append(option_type("List of devices"))
    backup_location = json.load(open("./data/setup_file.json", "r"))['backup_location']
    backups_list = os.listdir(f"{backup_location}/{device.get_mac().replace(':', '-')}")
    backups_list = [backup for backup in backups_list if backup.endswith(".ios")]

    def get_date(filename):
        return strptime(filename[:-4], "%Y-%m-%d-%H-%M-%S")

    backups_list = sorted(backups_list, key=get_date, reverse=True)
    i = 0
    backups = []
    for backup in backups_list:
        if i == 0:
            backups.append(backup_type(backup, i, True))
        else:
            backups.append(backup_type(backup, i))
        i += 1
    liste = list(backups + options, f"Choose a backup for {device.get_text()}", True, False)
    curses.wrapper(liste.executer)
    selected_backup = [backup for backup, checked in zip(liste.items, liste.checked) if checked][0]
    return selected_backup

def menu_item(backup: backup_type):
    if backup.get_index() == 0:
        options = [
            "See the current configuration",
            "Delete",
            "List of backup",
        ]
    else:
        options = [
            "Compare and upload",
            "Delete",
            "List of backup"
        ]
    liste = list([option_type(option) for option in options], backup.get_text(), True, False)
    curses.wrapper(liste.executer)
    selected_option = [device for device, checked in zip(liste.items, liste.checked) if checked][0]
    return selected_option

def compare(device_mod, index = 0):
    compareClass().read_files(device_mod.get_mac().replace(':', '-'), index)

def delete(selected_device, backup_delete):
    os.system("clear")
    response = 0
    while (response != "y" and response != "n"):
        response = input("Confirm delete (y/n): ")
    if response == "y":
        backup_location = json.load(open("./data/setup_file.json", "r"))['backup_location']
        os.remove(f"{backup_location}/{selected_device.get_mac().replace(':', '-')}/{backup_delete.get_name()}")
    os.system("clear")


def main():
    devices = load_devices()
    selected_device = device_list(devices)
    while selected_device.get_text() !=  "Quit":
        if selected_device.get_text() == "Make a backup for all devices":
            selected_device = device_list(devices)
        else:
            selected_backup = backup_list(selected_device)
            if selected_backup.get_text() == "Make a backup for this device":
                pass
            elif selected_backup.get_text() == "List of devices":
                selected_backup = 0
                selected_device = device_list(devices)
            else:
                selected_option = menu_item(selected_backup)
                match selected_option.get_text():
                    case "See the current configuration":
                        compare(selected_device)
                    case "Compare and upload":
                        compare(selected_device, selected_backup.get_index())
                    case "Compare and upload":
                        pass
                    case "Delete":
                        delete(selected_device, selected_backup)
                    case "List of backup":
                        pass
    os.system("clear")