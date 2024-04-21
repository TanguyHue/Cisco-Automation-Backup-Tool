import sys
sys.path.append("../..")
import os
from deamon.modules.deamon import stop_daemon

if __name__ == "__main__":
    os.system("sudo python3 ../../deamon/modules/deamon.py &")
    print("Démon démarré")
    input("Appuyez sur Entrée pour arrêter le démon")
    stop_daemon()

