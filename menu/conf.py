from setup.modules.list import listClass as list
from setup.modules.list_interface import interfaces
from setup.modules.list_scan import scanner
from setup.modules.save import saver
from setup.modules.liste_type import deviceType
from daemon_module.modules.daemonClass import stop_daemon
from backup.modules.backup import backup
import os
import curses
import json

def list_int():
    liste = list(interfaces().interface_address, 'List of network interface', True, False)
    curses.wrapper(liste.executer)
    selected_interfaces = [interface for interface, checked in zip(liste.items, liste.checked) if checked][0]
    print("Interface choosen:", selected_interfaces.get_name())
    return selected_interfaces

def list_device(interface):
    devices = scanner(f"{interface.get_address()}/{interface.get_cidr()}").scan()
    if devices.__len__() == 0:
        print("No devices found on the network.")
        return
    if devices.__len__() > 20:
        print("Too many devices found on the network. Only the first 20 will be displayed.")
        input("Press enter to continue...")
        devices.sort(key=lambda x: tuple(int(part) for part in x.get_ip().split('.')))
        devices = devices[:20]
    liste = list(devices, 'List of devices on the network', False, True)
    curses.wrapper(liste.executer)
    selected_devices = [device for device, checked in zip(liste.items, liste.checked) if checked]
    print("Devices saved")
    return selected_devices

def active_daemon():
    response=0
    stop_daemon()
    while response not in ['y', 'n', '']:
        response = input("Do you want to start the daemon ? (y/n) (default: y) ")
        location = input("Where is the daemon log ? (default: /tmp/log.txt) ")
        if location == '':
            location = "/tmp/log.txt"
        if response == 'y' or response == '':
            daemon = {
                "is_active": True,
                "daemon_location": "./daemon_module/modules/daemonClass.py",
                "daemon_log": location,
            }
            os.system("sudo python3 ./daemon_module/modules/daemonClass.py &")
            print("Daemon started")
        if response == 'n':
            daemon = {
                "is_active": False,
                "daemon_location": "./daemon_module/modules/daemonClass.py",
                "daemon_log": location,
            }
    return daemon

def conf_devices():
    response = 0
    while response not in ['y', 'n']:
        response = input("Is the username and password the same for all devices ? (y/n) ")
        if response == 'y':
            sameAccount = True
            username = input("Username: ")
            password = input("Password: ")
        if response == 'n':
            sameAccount = False
    response = 0
    while response not in ['y', 'n']:
        response = input("Is the enable password the same for all devices ? (y/n) ")
        if response == 'y':
            sameEnable = True
            enablePass = input("Enable password: ")
        if response == 'n':
            sameEnable = False

    devices = json.load(open("./data/devices.json"))
    for device in devices:
        list_type = list(deviceType().type_available, f"Type of device {device['ip']}", True, False)
        if not sameAccount:
            username = input(f"Username for {device['ip']} ({device['mac']}) ? ")
            password = input(f"Password for {device['ip']} ({device['mac']}) ? ") 
        if not sameEnable:
            enablePass = input(f"Enable password for {device['ip']} ({device['mac']}) ? ")

        curses.wrapper(list_type.executer)
        selected_type = [type for type, checked in zip(list_type.items, list_type.checked) if checked][0]
        device['type'] = selected_type.get_type()
        device['username'] = username
        device['password'] = password
        device['enable_password'] = enablePass

    json.dump(devices, open("./data/devices.json", 'w'), indent=4)

def main():
    init = True
    if saver().is_configured():
        response = 0
        while response not in ['y', 'n']:
            response = input("Configuration already exists. Do you want to overwrite it ? (y/n) ")
            if response == 'n':
                init = False

    if init:
        selected_interfaces = list_int()
        selected_devices = list_device(selected_interfaces)
        saver().save_devices(selected_devices)
        daemon = active_daemon()
        conf_devices()

        print("Just press enter to select the default value")
        response = -1
        while response < 0 or response > 24:
            response = (input("How often do you want to save the data ? (in hours) (default: 0) "))
            if response == '':
                response = 0
            else:
                try:
                    response = int(response)
                except ValueError:
                    response = -1
        delay_hour = response
        while response < 1 or response > 59:
            response = (input("How often do you want to save the data ? (in minutes) (default: 2) "))
            if response == '':
                response = 2
            else:
                try:
                    response = int(response)
                except ValueError:
                    response = -1
        delay_minute = response
        response = input("Where do you want to save the backup ? (default: ./data/backup) ")
        if response == '':
            response = "./data/backup"
        backup_location = response
        response = input("Where do you want to save the devices file ? (default: ./data/devices.json) ")
        if response == '':
            response = "./data/devices.json"
        devices_location = response
        response = input("Where is the crontab file ? (default: /etc/crontab) ")
        if response == '':
            response = "/etc/crontab"
        crontab_location = response
        saver().save_setup(selected_interfaces, daemon, delay_hour, delay_minute, 
                           devices_location, backup_location, crontab_location)
        print("Configuration saved")

        backupFile = backup(backup_location, devices_location)
        response = 0
        while response not in ['y', 'n', '']:
            response = input("Do you want to erase previous backups ? (y/n) (default: n) ")
            if response == 'y':
                backupFile.reset()
        backupFile.save()

    print("Configuration finished")
    input("Press enter to continue...")
    os.system("clear")