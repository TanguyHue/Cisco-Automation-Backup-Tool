from json import load
import os
import threading
from time import strftime, sleep
from crontab import CronTab
import sys
from netmiko import ConnectHandler

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
    
    if device_info["type"] == "other":
        print("Device type not supported")
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
        class save_backup:
            def __init__(self, device, backup_location):
                self.device = device
                self.backup_location = backup_location
            def run(self):
                self.backup(self.device, self.backup_location)
            def backup(self, device, backup_location):
                command = 'show running-config'
                os.system("clear")
                self.test_connection = False
                def afficher_attente():
                    while True and not self.test_connection:
                        for i in range(3):
                            print(f"Test of SSH connection to {device_info['ip']}" + "." * (i + 1), end="\r")
                            sleep(0.4)
                            print("\033[K", end="")
                thread = threading.Thread(target=afficher_attente)
                thread.daemon = True
                thread.start()
                try:
                    net_connect = ConnectHandler(**device)
                    net_connect.enable()
                    output = net_connect.send_command(command)
                    print(f"{command}:\n{output[:10]}...\n")
                    net_connect.disconnect()          
                    self.test_connection = True
                    thread.join()
                    current_time = strftime("%Y-%m-%d-%H-%M-%S")
                    
                    if not os.path.exists(backup_location):
                        os.makedirs(backup_location)
                    with open(f"{backup_location}/{current_time}.ios", 'w') as f:
                        f.write(output)
                except Exception as e:   
                    os.system("clear")                  
                    self.test_connection = True
                    thread.join()
                    print(f"Error backing up {device_info['mac']}\n")
                    print(e)
                    input("Press enter to continue")
        save_backup(device, backup_location).run()
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

def add_daemon():
    remove_daemon()
    parameters = load(open("./data/setup_file.json", "r"))
    crontab_location = parameters["crontab_location"]
    cron = CronTab(tabfile=crontab_location)
    cron.write()
    job = cron.new(command=f'python3 {os.getcwd()}/daemon_module/modules/daemonClass.py &')
    job.setall('@reboot')
    job.set_comment(f'Daemon reboot of Cisco Automation Tool')
    cron.write()

def remove_daemon():
    parameters = load(open("./data/setup_file.json", "r"))
    crontab_location = parameters["crontab_location"]
    cron = CronTab(tabfile=crontab_location)
    jobs_to_remove = [job for job in cron if job.comment.startswith("Daemon reboot of Cisco Automation Tool")]
    if jobs_to_remove is not None:
        cron.remove(jobs_to_remove[0])
    cron.write()

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

