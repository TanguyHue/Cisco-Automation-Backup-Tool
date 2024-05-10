import sys
sys.path.append("../..")
import os
from daemon.modules.daemon import stop_daemon

if __name__ == "__main__":
    os.system("sudo python3 ../../daemon/modules/daemon.py &")
    print("daemon started")
    input("Press enter to stop the daemon\n")
    stop_daemon()

