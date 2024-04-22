import menu.conf as conf
import menu.scan as scan
from menu.list_menu import menu_list
from menu.list_device import main as list_device
from setup.modules.save import saver
from setup.modules.list import ListeAvecCases as list
import curses

if __name__ == '__main__':
    if not saver().is_configured():
        conf.main()
    
    liste = list(menu_list().item_menu, 'Menu principal', True, False)
    curses.wrapper(liste.executer)
    selected_item = [item for item, checked in zip(liste.items, liste.checked) if checked][0].get_value()

    while selected_item != 4:
        match selected_item:
            case 0:
                print("Configuration")
                conf.main()
            case 1:
                print("Liste des appareils")
                list_device()
            case 2:
                print("Scan")
                scan.main()
            case 4:
                print("Au revoir")
            case default:
                print("Non implémenté")
        liste = list(menu_list().item_menu, 'Menu principal', True, False)
        curses.wrapper(liste.executer)
        selected_item = [item for item, checked in zip(liste.items, liste.checked) if checked][0].get_value()   
         