import json
import os
from setup.modules.device import device as device_type
from setup.modules.list import ListeAvecCases as list
from setup.modules.liste_type import deviceType
import curses

class option_type:
    def __init__(self, text) -> None:
        self.text = text

    def get_text(self):
        return self.text

def load(path="./data/devices.json"):
    with open(path, "r") as file:
        devices_load = json.load(file)
    devices = []
    for device in devices_load:
        devices.append(device_type(device['ip'], device['mac'], device['type'], device['username'], device['password']))
    return devices

def menu_list(devices):
    quit = []
    quit.append(option_type("Quit"))
    liste = list(devices + quit, 'List of devices', True, False)
    curses.wrapper(liste.executer)
    selected_device = [device for device, checked in zip(liste.items, liste.checked) if checked][0]
    return selected_device

def menu_item(device):
    options = [
        "Edit",
        "Delete",
        "Back"
    ]
    liste = list([option_type(option) for option in options], device.get_text(), True, False)
    curses.wrapper(liste.executer)
    selected_option = [device for device, checked in zip(liste.items, liste.checked) if checked][0]
    return selected_option

def modifier(device_mod):
    os.system("clear")
    print(f"Edit the device: {device_mod.get_text()}")
    print("Press enter to keep the same value")

    new_username = input(f"Username for {device_mod.get_ip()} ? ({device_mod.get_username()})")
    if new_username == "":
        new_username = device_mod.get_username()
    new_password = input(f"Password for {device_mod.get_ip()} ? ({device_mod.get_password()})") 
    if new_password == "":
        new_password = device_mod.get_password()

    list_type = list(deviceType().type_available, f"Type fo device {device_mod.get_ip()} ({device_mod.get_type_name()})", True, False)
    curses.wrapper(list_type.executer)
    selected_type = [type for type, checked in zip(list_type.items, list_type.checked) if checked][0]
    new_type = selected_type.get_type()

    device_mod.set_info(new_type, new_username, new_password)
    devices = load()

    os.system("clear")
    new_devices = [device if device.get_mac() != device_mod.get_mac() else device_mod for device in devices]
    with open("./data/devices.json", "w") as file:
        json.dump([device.get_full_info() for device in new_devices], file, indent=4)

def delete(device_delete):
    devices = load()
    new_devices = [device for device in devices if device.get_mac() != device_delete.get_mac()]
    with open("./data/devices.json", "w") as file:
        json.dump([device.get_full_info() for device in new_devices], file, indent=4)


def main():
    devices = load()
    selected_device = menu_list(devices)
    while selected_device.get_text() != "Quit":
        selected_option = menu_item(selected_device)
        match selected_option.get_text():
            case "Edit":
                modifier(selected_device)
            case "Delete":
                delete(selected_device)
        devices = load()
        selected_device = menu_list(devices)