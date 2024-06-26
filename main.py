from os import remove, system
import menu.conf as conf
import menu.scan as scan
from menu.list_menu import menu_list
from menu.list_device import main as list_device
from menu.list_saves import main as list_saves
from backup.modules.backup import backup
from setup.modules.save import saver
from setup.modules.list import listClass as list
from setup.modules.cron import save_cron, remove_cron
from daemon_module.modules.daemonClass import start_daemon, stop_daemon
from daemon_module.modules.daemonClass import status as daemon_status
import curses

if __name__ == '__main__':
    if not saver().is_configured():
        conf.main()
    
    liste = list(menu_list().item_menu, 'Main Menu', True, False)
    curses.wrapper(liste.executer)
    selected_item = [item for item, checked in zip(liste.items, liste.checked) if checked][0].get_value()
    quit_option = menu_list().length() - 1

    while selected_item != quit_option:
        match selected_item:
            case 0:
                print("Configuration")
                conf.main()
            case 1:
                print("List of devices")
                list_device()
            case 2:
                print("Scan")
                scan.main()
            case 3:
                print("List of saves")
                list_saves()
            case 4:
                system("clear")
                response = input("Where are the backups ? (default: ./data/backup) ")
                if response == '':
                    response = "./data/backup"
                backup_location = response
                response = input("Where is the device file ? (default: ./data/devices.json) ")
                if response == '':
                    response = "./data/devices.json"
                devices_location = response
                backup(backup_location, devices_location).reset()
                remove("./data/setup_file.json")
                remove(devices_location)
                response = 0
                while response not in ['y', 'n', '']:
                    response = input("Do you want to remake the configuration now ? (y/n) (default: y) ")
                    if response == 'y' or response == '':
                        conf.main()
                    else:
                        system("clear")
                        selected_item = quit_option               
                print("Reset configuration")
            case 5:
                print("Cron")
                save_cron()
                system("clear")
            case 6:
                print("Cron")
                remove_cron()
                system("clear")
            case 7:
                print("Daemon status")
                daemon_status()
                system("clear")
            case 8:
                stop_daemon()
                start_daemon()
                print("Relaunch daemon")
            case default:
                print("Goodbye !")
        
        if selected_item != quit_option:
            liste = list(menu_list().item_menu, 'Main Menu', True, False)
            curses.wrapper(liste.executer)
            selected_item = [item for item, checked in zip(liste.items, liste.checked) if checked][0].get_value()   
         