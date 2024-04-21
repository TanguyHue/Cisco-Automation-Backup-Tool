import sys
sys.path.append("../..")
from backup.modules.backup import backup

if __name__ == "__main__":
    backupFile = backup("./data_test", "../../data/devices.json")
    backupFile.save()