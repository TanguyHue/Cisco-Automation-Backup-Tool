import sys
sys.path.append("../..")
import os
from deamon.modules.deamon import stop_daemon

if __name__ == "__main__":
    os.system("sudo python3 ../../deamon/modules/deamon.py &")
    print("Deamon started")
    input("Press enter to stop the deamon\n")
    stop_daemon()

