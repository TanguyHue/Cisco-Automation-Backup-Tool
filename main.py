from setup.modules.list import ListeAvecCases as list
from setup.modules.list_interface import interfaces
from setup.modules.list_scan import scanner
from setup.modules.save import saver
from deamon.modules.deamon import stop_daemon
from backup.modules.backup import backup
import os
import curses

if __name__ == '__main__':
    init = True
    # Vérifier s'il y a déjà un fichier de configuration
    if saver().is_configured():
        response = 0
        while response not in ['o', 'n']:
            response = input("Configuration déjà enregistrée\nVoulez-vous la réinitialiser ? (o/n) ")
            if response == 'n':
                init = False

    if init:
        # Lister interfaces réseaux
        liste = list(interfaces().interface_address, 'Liste des interfaces réseau', True, False)
        curses.wrapper(liste.executer)
        selected_interfaces = [interface for interface, checked in zip(liste.items, liste.checked) if checked][0]
        print("Interfaces sélectionnées:", selected_interfaces.get_name())

        # Scanner le réseau
        liste = list(scanner(f"{selected_interfaces.get_address()}/{selected_interfaces.get_cidr()}").scan(), 'Liste des appareils sur le réseau', False, True)
        curses.wrapper(liste.executer)
        selected_devices = [device for device, checked in zip(liste.items, liste.checked) if checked]
        saver().save_devices(selected_devices)
        print("Appareils enregistrés")

        # Enregistrer la configuration
        response=0
        stop_daemon()
        while response not in ['o', 'n', '']:
            response = input("Voulez-vous activer l'enregistrement manuel via un ping au serveur (oui par defaut) ? (o/n) ")
            if response == 'o' or response == '':
                deamon = {
                    "is_active": True,
                    "deamon_location": "./deamon/modules/deamon.py",
                    "deamon_log": "/tmp/log.txt",
                }
                os.system("sudo python3 ./deamon/modules/deamon.py &")
                print("Démon démarré")
            if response == 'n':
                deamon = {
                    "is_active": False,
                }
        saver().save_setup(selected_interfaces, deamon)
        print("Configuration enregistrée")
    
    # Sauvegarde des appareils
    backupFile = backup("./data/backup", "./data/devices.json")
    backupFile.reset()
    backupFile.save()