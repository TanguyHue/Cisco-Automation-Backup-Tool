import os

if __name__ == "__main__":
    os.system("sudo python3 ../../deamon/modules/deamon.py &")
    print("Démon démarré")
    input("Appuyez sur Entrée pour arrêter le démon")
    os.system("sudo pkill -f deamon.py")

