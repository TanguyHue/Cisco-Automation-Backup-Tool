from json import load
import os
from crontab import CronTab
import sys

def backup(backup_location, devices_file, save_backup):
    if save_backup:
        mac_address = backup_location.split('/')[-1].replace("-", ":")
    else:
        mac_address = backup_location.split('/')[-2].replace("-", ":")
    devices_list = load(open(devices_file, "r"))
    found = False
    print(f"Backing up {mac_address}")
    
    for device in devices_list:
        if device['mac'] == mac_address:
            device_info = device
            found = True

    if not found:
        print("Device not found")
        return

    device = {
        'device_type': device_info["type"],
        'ip': device_info["ip"],
        'username': device_info["username"], 
        'password': device_info["password"], 
        'secret': device_info["enable_password"]
    }

    print(device)

    if save_backup:
        pass
    else:
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

def save_cron(mac_address_list = [], enter = True):
    if enter:
        os.system("clear")
    parameters = load(open("./data/setup_file.json", "r"))
    crontab_location = parameters["crontab_location"]
    delay_hour = parameters["delay_hour"]
    delay_minute = parameters["delay_minute"]
    current_location = os.getcwd()
    cron = CronTab(tabfile=crontab_location)
    if len(mac_address_list) == 0:
        devices_file = parameters["devices_list_location"]
        devices_list = load(open(devices_file, "r"))
        for device in devices_list:
            mac_address_list.append(device["mac"])
    remove_cron(False)
    for mac_address in mac_address_list:

        if delay_hour == 0:
            delay_hour = '*'
        job = cron.new(command=f'python3 {current_location}/setup/modules/cron.py 0 {mac_address}')
        job.setall(f'{delay_minute} {delay_hour} * * *')
        job.set_comment(f'Cisco automation tool: {mac_address} backup')
        cron.write()
        if enter:
            print(f'Jobs for {mac_address} added')

    if enter:
        input("Press enter to continue")
    else:
        print("Jobs added")
    
def remove_cron(enter = True):
    if enter:
        os.system("clear")
    parameters = load(open("./data/setup_file.json", "r"))
    crontab_location = parameters["crontab_location"]
    cron = CronTab(tabfile=crontab_location)
    jobs_to_remove = [job for job in cron if job.comment.startswith("Cisco automation tool:")]
    if enter:
        print(f'Removing {len(jobs_to_remove)} jobs')
    for job in jobs_to_remove:
        cron.remove(job)
    cron.write()
    if enter:
        print("Jobs removed")
        input("Press enter to continue")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 cron.py [0 : save | 1 : set] ...")
        print("If save : python3 cron.py 0 <mac_address1> <mac_address2> ...")
        print("If set : python3 cron.py 1 <mac_address> <file_name>")
        sys.exit(1)
    if sys.argv[1] == "0":
        for mac_address in sys.argv[2:]:
            backup_location = load(open("./data/setup_file.json", "r"))["backup_location"] + f"/{mac_address}"
            print(f"Backing up {backup_location}")
            devices_file = load(open("./data/setup_file.json", "r"))["devices_list_location"]
            backup(backup_location, devices_file, True)
    elif sys.argv[1] == "1":
        for mac_address, file_name in sys.argv[2:]:
            backup_location = load(open("./data/setup_file.json", "r"))["backup_location"] + f"/{mac_address}/{file_name}"
            print(f"Backing up {backup_location}")
            devices_file = load(open("./data/setup_file.json", "r"))["devices_list_location"]
            backup(backup_location, devices_file, False)
    else:
        print("Error: Invalid arguments")

