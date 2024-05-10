import json
import socket
import struct
import datetime
import daemon
import os

class pingDetect:
    def __init__(self, log_file='/tmp/log.txt'):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        self.log_file = log_file

    def start(self):
        with open(self.log_file, 'a') as log_file:
            while True:
                packet, _ = self.sock.recvfrom(1024)
                
                icmp_type = struct.unpack('!BB', packet[20:22])[0]
                
                if icmp_type == 8:
                    ip_header = packet[0:20]
                    iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
                    source_ip = socket.inet_ntoa(iph[8])
                    
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    log_file.write(f"{current_time} | Ping from: {source_ip}\n")
                    log_file.flush()
                    
class pingDaemon:
    def __init__(self) -> None:
        pass

    def start(self):
        self.pid = os.getpid()
        with daemon.DaemonContext(
            stdout=open('/tmp/stdout.txt', 'w+'),
            stderr=open('/tmp/stderr.txt', 'w+'),
            stdin=open('/dev/null', 'r')
        ):
            pingDetect().start()
    
def stop_daemon():
    os.system("sudo pkill -f daemon.py")

def status():
    daemon = json.load(open("./data/setup_file.json", "r"))["daemon"]
    print(f'Daemon log: {daemon["daemon_log"]}')
    print(f'Daemon location: {daemon["daemon_location"]}')
    if daemon["is_active"]:
        print("Daemon is running")
    else:
        print("Daemon is not running")
    print("\nLast 10 logs:")
    with open(daemon["daemon_log"], 'r') as log_file:
        lines = log_file.readlines()
        for line in lines[-10:]:
            print(line)
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
        config = json.load(open("./data/setup_file.json", "r"))
        config["daemon"]["is_active"] = True
        json.dump(config, open("./data/setup_file.json", "w+"), indent=4)
        os.system("sudo python3 ./daemon_module/modules/daemonClass.py &")
        input("Daemon stopped. Press enter to exit")
    
if __name__ == "__main__":
    pingDaemon().start()