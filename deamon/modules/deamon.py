import socket
import struct
import datetime
import daemon
import os

class pingDetect:
    def __init__(self, log_file='/tmp/log.txt'):
        # Créer une socket ICMP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        self.log_file = log_file

    def start(self):
        with open(self.log_file, 'a') as log_file:
            # Écouter les paquets ICMP
            while True:
                packet, _ = self.sock.recvfrom(1024)
                
                # Extraire le type de message ICMP
                icmp_type = struct.unpack('!BB', packet[20:22])[0]
                
                # Si le type de message ICMP est 8, il s'agit d'un ping
                if icmp_type == 8:
                    # Extraire l'adresse IP de l'en-tête IP
                    ip_header = packet[0:20]
                    iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
                    source_ip = socket.inet_ntoa(iph[8])
                    
                    # Écrire dans le fichier de log
                    # Obtenir la date et l'heure actuelles
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Écrire dans le fichier de log avec la date et l'heure
                    log_file.write(f"{current_time} | Ping reçu de: {source_ip}\n")
                    log_file.flush()  # Force l'écriture immédiate dans le fichier
                    
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