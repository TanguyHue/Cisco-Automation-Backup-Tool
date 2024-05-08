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

                    log_file.write(f"{current_time} | Ping reçu de: {source_ip}\n")
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
    os.system("sudo pkill -f deamon.py")

if __name__ == "__main__":
    pingDaemon().start()