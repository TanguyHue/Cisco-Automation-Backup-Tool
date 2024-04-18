#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#define PACKET_SIZE 4096

int main() {
    int sockfd;
    struct sockaddr_in addr;
    char packet[PACKET_SIZE];
    socklen_t addr_len = sizeof(addr);

    // Créer une socket ICMP
    sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
    if (sockfd < 0) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    // Écouter les paquets ICMP
    while (1) {
        ssize_t packet_size = recvfrom(sockfd, packet, PACKET_SIZE, 0,
                                        (struct sockaddr *)&addr, &addr_len);
        if (packet_size < 0) {
            perror("recvfrom");
            exit(EXIT_FAILURE);
        }

        // Extraire le type de message ICMP
        struct icmphdr *icmp_header = (struct icmphdr *)(packet + 20);
        unsigned char icmp_type = icmp_header->type;

        // Si le type de message ICMP est 8, il s'agit d'un ping
        if (icmp_type == ICMP_ECHO) {
            // Extraire l'adresse IP de l'en-tête IP
            struct iphdr *ip_header = (struct iphdr *)packet;
            struct in_addr source_ip_addr;
            source_ip_addr.s_addr = ip_header->saddr;
            char *source_ip = inet_ntoa(source_ip_addr);
            if (source_ip == NULL) {
                perror("inet_ntoa");
                exit(EXIT_FAILURE);
            }

            printf("Ping reçu de: %s\n", source_ip);
        }
    }

    return 0;
}
