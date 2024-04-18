import socket
import struct

# Créer une socket ICMP
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

# Écouter les paquets ICMP
while True:
    packet, addr = sock.recvfrom(1024)
    
    # Extraire le type de message ICMP
    icmp_type = struct.unpack('!BB', packet[20:22])[0]
    
    # Si le type de message ICMP est 8, il s'agit d'un ping
    if icmp_type == 8:
        # Extraire l'adresse IP de l'en-tête IP
        ip_header = packet[0:20]
        iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
        source_ip = socket.inet_ntoa(iph[8])
        
        print("Ping reçu de:", source_ip)
