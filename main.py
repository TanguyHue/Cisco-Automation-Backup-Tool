from setup.modules.list import ListeAvecCases as list
from setup.modules.list_interface import interfaces
from setup.modules.list_scan import scanner
import curses

if __name__ == '__main__':
    liste = list(interfaces().interface_address, True, False)
    curses.wrapper(liste.executer)
    selected_interfaces = [interface for interface, checked in zip(liste.items, liste.checked) if checked][0]
    print("Interfaces sélectionnées:", selected_interfaces['interface'])
    liste = list(scanner(f"{selected_interfaces['ipv4_address']}/{selected_interfaces['cidr']}").scan(), False, True)
    curses.wrapper(liste.executer)
    selected_devices = [device for device, checked in zip(liste.items, liste.checked) if checked]
    print("Appareil sélectionné:",  selected_devices)