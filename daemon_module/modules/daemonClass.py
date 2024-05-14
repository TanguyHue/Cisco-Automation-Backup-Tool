#!/usr/bin/python3

import json
import socket
import struct
import datetime
import subprocess
import sys
import daemon
import os

class pingDetect:
    def __init__(self, log_file):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        self.log_file = log_file
        self.recent_pings = {}

    def start(self):
        with open(self.log_file, 'a') as log_file:
            while True:
                packet, _ = self.sock.recvfrom(1024)
                
                icmp_type = struct.unpack('!BB', packet[20:22])[0]
                
                if icmp_type == 8:
                    ip_header = packet[0:20]
                    iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
                    source_ip = socket.inet_ntoa(iph[8])
                    
                    current_time = datetime.datetime.now()
                    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

                    if source_ip in self.recent_pings:
                        last_ping_time = self.recent_pings[source_ip]
                        if (current_time - last_ping_time).total_seconds() < 10:
                            continue
                    self.recent_pings[source_ip] = current_time
                    log_file.write(f"{formatted_time} | Ping from: {source_ip}\n")

                    list_devices = json.load(open("./data/setup_file.json", "r"))["devices_list_location"]
                    list_devices = json.load(open(list_devices, "r"))
                    found = False
                    for device in list_devices:
                        if device["ip"] == source_ip:
                            found = True
                            error_file_path = "/tmp/error.txt"
                            with open(error_file_path, 'a') as error_file:
                                error_file.write(f'Backup saved for : {device["mac"]}\n')
                                error_file.flush() 
                            initial_size = os.path.getsize(error_file_path)
                            command = f'python3 ./setup/modules/cron.py 0 {device["mac"]}'
                            subprocess.run(command, shell=True, stderr=open(error_file_path, 'a'))
                            
                            new_size = os.path.getsize(error_file_path)
                            if new_size != initial_size:
                                formatted_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                log_file.write(f"Error in cron program for : {device['mac']}\n")
                                log_file.write(f"Error dated : {formatted_time}\n")

                                with open(error_file_path, 'a') as error_file:
                                    error_file.write(f"Error dated : {formatted_time}\n======================================\n\n")
                                    error_file.flush() 
                            else:
                                log_file.write(f"No error detected\n")

                    if not found:
                        log_file.write("Device not found in list\n")
                    
class pingDaemon:
    def __init__(self) -> None:
        pass

    def start(self, log_file='/tmp/log.txt'):
        if os.path.exists(log_file):
            os.system(f"sudo chmod 666 {log_file}")
        if os.path.exists("/tmp/stdout.txt"):
            os.system(f"sudo rm /tmp/stdout.txt")
        if os.path.exists("/tmp/stderr.txt"):
            os.system(f"sudo rm /tmp/stderr.txt")
        self.pid = os.getpid()
        with daemon.DaemonContext(
            working_directory=os.getcwd(),
            stdout=open('/tmp/stdout.txt', 'w+'),
            stderr=open('/tmp/stderr.txt', 'w+'),
            stdin=open('/dev/null', 'r')
        ):
            pingDetect(log_file).start()
    
def stop_daemon():
    os.system("sudo pkill -f daemonClass.py")

def start_daemon():
    daemon = json.load(open("./data/setup_file.json", "r"))["daemon"]
    os.system(f"sudo python3 ./daemon_module/modules/daemonClass.py {daemon['daemon_log']} 2> /tmp/error.txt &")

def status():
    daemon = json.load(open("./data/setup_file.json", "r"))["daemon"]
    if daemon["is_active"]:
        print("\033[92m✓ Daemon is running\033[0m")
    else:
        print("\033[91m✗ Daemon is not running\033[0m")

    print(f'Daemon log: {daemon["daemon_log"]}')
    print(f'Daemon location: {daemon["daemon_location"]}')
    print("\nLast 10 logs:")
    with open(daemon["daemon_log"], 'r') as log_file:
        lines = log_file.readlines()
        for line in lines[-10:]:
            print(line, end="")
    if os.path.exists("/tmp/stderr.txt") and os.path.getsize("/tmp/stderr.txt") > 0:
        print("Error logs:")
        with open("/tmp/stderr.txt", 'r') as log_file:
            lines = log_file.readlines()
            for line in lines:
                print(line, end="")
    print('\nError of cron programm are stored in /tmp/error.txt')
    response = 0
    while response != "1" and response != "2":
        if daemon["is_active"]:
            response = input("1. Stop daemon | 2. Exit : ")
        else:
            response = input("1. Start daemon | 2. Exit : ")
    
    if daemon["is_active"] and response == "1":
        stop_daemon()
        config = json.load(open("./data/setup_file.json", "r"))
        config["daemon"]["is_active"] = False
        json.dump(config, open("./data/setup_file.json", "w+"), indent=4)
        input("Daemon stopped. Press enter to exit")
    elif not daemon["is_active"] and response == "1":
        start_daemon()
        config = json.load(open("./data/setup_file.json", "r"))
        config["daemon"]["is_active"] = True
        json.dump(config, open("./data/setup_file.json", "w+"), indent=4)
        input("Daemon started. Press enter to exit")
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        pingDaemon().start(sys.argv[1])
    else:
        pingDaemon().start()