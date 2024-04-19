import sys
sys.path.append("..")

import curses
from modules.list_interface import interfaces
from modules.list import ListeAvecCases

if __name__ == "__main__":
    liste = ListeAvecCases(interfaces().interface_address, True, False)
    curses.wrapper(liste.executer)
    selected_interfaces = [interface['interface'] for interface, checked in zip(liste.items, liste.checked) if checked]
    print("Interfaces sélectionnées:", selected_interfaces)
