import netifaces
import curses 
import ipaddress

# Getting interfaces 
interfaces = netifaces.interfaces()
interface_address = []

for interface in interfaces: 
    ipv4_info = netifaces.ifaddresses(interface).get(netifaces.AF_INET)
    if ipv4_info:
        ipv4_address = ipv4_info[0]['addr']
        netmask = ipv4_info[0]['netmask']
        if ipv4_info[0].get('broadcast') is not None:
          broadcast = ipv4_info[0]['broadcast']
          network_address = ipaddress.IPv4Network(f"{ipv4_address}/{netmask}", strict=False).network_address
          text = f"{interface}: Network {network_address} | IP Address {ipv4_address} | Broadcast {broadcast}"
          interface_address.append({
            'interface': interface, 
            'network_address': network_address, 
            'ipv4_address': ipv4_address, 
            'broadcast': broadcast,
            'text': text,
            })
 
class ListeAvecCases:
    def __init__(self, items):
        self.items = items
        self.checked = [False] * len(items)
        self.selected_index = 0
        self.prev_selected_index = None  # Keep track of the previously selected index

    def afficher(self, stdscr):
        stdscr.clear()
        for i, item in enumerate(self.items):
            checked = 'X' if self.checked[i] else ' '
            if i == self.selected_index:
                stdscr.addstr(f"> ({checked}) {item['text']}\n", curses.color_pair(1))
            else:
                stdscr.addstr(f"  ({checked}) {item['text']}\n")

    def cocher_decocher(self, index):
        # Uncheck the previously selected interface (if any)
        if self.prev_selected_index is not None:
            self.checked[self.prev_selected_index] = False
        # Check the newly selected interface
        self.checked[index] = True
        # Update the previously selected index
        self.prev_selected_index = index

    def executer(self, stdscr):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        while True:
            self.afficher(stdscr)
            stdscr.addstr(len(self.items) + 1, 2, "Appuyez sur espace pour sélectionner, ou Entrée pour valider.")
            key = stdscr.getch()
            if (key == curses.KEY_ENTER or key in [10, 13]) and any(self.checked):
                break
            elif key == curses.KEY_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.items)
            elif key == curses.KEY_UP:
                self.selected_index = (self.selected_index - 1) % len(self.items)
            elif key == ord(' '):
                self.cocher_decocher(self.selected_index)

if __name__ == "__main__":
    liste = ListeAvecCases(interface_address)
    curses.wrapper(liste.executer)
    selected_interfaces = [interface['interface'] for interface, checked in zip(liste.items, liste.checked) if checked]
    print("Interfaces sélectionnées:", selected_interfaces)
