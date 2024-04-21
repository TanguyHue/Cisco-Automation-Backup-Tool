from setup.modules.list import ListeAvecCases as list
from setup.modules.list_interface import interfaces
from setup.modules.list_scan import scanner
from setup.modules.save import saver
from setup.modules.liste_type import deviceType
from deamon.modules.deamon import stop_daemon
from backup.modules.backup import backup
import os
import curses
import json

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

        response = 0
        while response not in ['o', 'n']:
            response = input("Le nom d'utilisateur et le mot de passe sont-ils identiques pour tous les appareils ? (o/n) ")
            if response == 'o':
                same = True
                username = input(f"Nom d'utilisateur: ")
                password = input(f"Mot de passe: ")
            if response == 'n':
                same = False

        devices = json.load(open("./data/devices.json"))
        for device in devices:
            list_type = list(deviceType().type_available, f"Type de l\'appareil {device['ip']}", True, False)
            if not same:
                username = input(f"Nom d'utilisateur pour {device['ip']} ({device['mac']}) ? ")
                password = input(f"Mot de passe pour {device['ip']} ({device['mac']}) ? ") 

            curses.wrapper(list_type.executer)
            selected_type = [type for type, checked in zip(list_type.items, list_type.checked) if checked][0]
            device['type'] = selected_type.get_type()
            device['username'] = username
            device['password'] = password
    
        json.dump(devices, open("./data/devices.json", 'w'), indent=4)


        response = -1
        while response < 0 or response > 24:
            response = (input("Quels délais entre chaque récupération des données (en heures) (Par défaut, à 5) ? (1-24) "))
            if response == '':
                response = 5
            else:
                try:
                    response = int(response)
                except ValueError:
                    response = -1

        saver().save_setup(selected_interfaces, deamon, response)
        print("Configuration enregistrée")
    
    # Sauvegarde des appareils
    backupFile = backup("./data/backup", "./data/devices.json")
    backupFile.reset()
    backupFile.save()