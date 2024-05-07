import sys
sys.path.append("../..")


from file_comparaison.modules.compare import compareClass
import os
import json
import time
from shutil import copyfile, rmtree

if __name__ == '__main__':
    backup_location = json.load(open("../../data/setup_file.json", "r"))['backup_location']
    if not os.path.exists(f"../../{backup_location}00-00-00"):
        os.mkdir(f"../../{backup_location}00-00-00")
    current_time = time.strftime("%Y-%m-%d-%H-%M-%S")
    last_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time() - 60))
    copyfile("./cisco/s1.ios", f"../../{backup_location}00-00-00/{current_time}.ios")
    copyfile("./cisco/s2.ios", f"../../{backup_location}00-00-00/{last_time}.ios")

    compareClass().read_files('00-00-00', 1)

    rmtree(f"../../{backup_location}00-00-00")