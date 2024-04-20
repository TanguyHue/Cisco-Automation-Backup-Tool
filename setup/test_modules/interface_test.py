import sys
sys.path.append("../..")

import curses
from setup.modules.list_interface import interfaces
from setup.modules.list import ListeAvecCases

if __name__ == "__main__":
    liste = ListeAvecCases(interfaces().interface_address, 'Liste des interfaces réseau', True, False)
    curses.wrapper(liste.executer)
    selected_interfaces = [interface.get_name() for interface, checked in zip(liste.items, liste.checked) if checked]
    print("Interfaces sélectionnées:", selected_interfaces)
