import curses
import scapy.all as scapy
import time
import threading

target_ip = "172.23.51.75/20"
scan_terminé = False

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    results = []

    for element in answered_list:
        result = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        results.append(result)
    
    return results

class ListeAvecCases:
    def __init__(self, items):
        self.items = items
        self.checked = [True] * len(items)
        self.selected_index = 0

    def afficher(self, stdscr):
        for i, item in enumerate(self.items):
            checked = 'X' if self.checked[i] else ' '
            if i == self.selected_index:
                stdscr.addstr(f"> [{checked}] {item}\n", curses.color_pair(1))
            else:
                stdscr.addstr(f"  [{checked}] {item}\n")

    def cocher_decocher(self, index):
        self.checked[index] = not self.checked[index]

    def executer(self, stdscr):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Liste des appareils détectés\n\n")
            self.afficher(stdscr)
            stdscr.addstr(len(self.items) + 3, 0, "Appuyez sur espace pour cocher/décocher, ou Entrée pour valider.")
            key = stdscr.getch()
            if key == curses.KEY_ENTER or key in [10, 13]:
                break
            elif key == curses.KEY_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.items)
            elif key == curses.KEY_UP:
                self.selected_index = (self.selected_index - 1) % len(self.items)
            elif key == ord(' '):
                self.cocher_decocher(self.selected_index)

if __name__ == "__main__":
    # Fonction pour afficher les trois points en boucle
    def afficher_attente():
        while True and not scan_terminé:
            for i in range(3):
                print("Scan en cours" + "." * (i + 1), end="\r")
                time.sleep(0.5)
                print("\033[K", end="")

    # Démarrer l'affichage en attente en arrière-plan
    thread = threading.Thread(target=afficher_attente)
    thread.daemon = True
    thread.start()
    
    # Effectuer le scan
    scan_results = scan(target_ip)
    scan_terminé = True
    
    # Arrêter l'affichage en attente
    thread.join()
    
    # Créer une instance de ListeAvecCases avec les résultats du scan
    liste = ListeAvecCases(scan_results)
    
    # Exécuter la liste dans curses
    curses.wrapper(liste.executer)
