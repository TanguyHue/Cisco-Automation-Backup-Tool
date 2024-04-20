from setup.modules.list import ListeAvecCases as list
from setup.modules.list_interface import interfaces
from setup.modules.list_scan import scanner
from setup.modules.save import saver
import curses

if __name__ == '__main__':
    liste = list(interfaces().interface_address, True, False)
    curses.wrapper(liste.executer)
    selected_interfaces = [interface for interface, checked in zip(liste.items, liste.checked) if checked][0]
    print("Interfaces sélectionnées:", selected_interfaces.get_name())
    liste = list(scanner(f"{selected_interfaces.get_address()}/{selected_interfaces.get_cidr()}").scan(), False, True)
    curses.wrapper(liste.executer)
    selected_devices = [device for device, checked in zip(liste.items, liste.checked) if checked]
    saver().save_devices(selected_devices)
    saver().save_setup(selected_interfaces)
    print("Appareils enregistrés")