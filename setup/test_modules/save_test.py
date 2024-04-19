import sys
sys.path.append("..")

from modules.save import saver

if __name__ == "__main__":
    setup = {
        "interface": "eth0",
        "network": "192.168.1.0",
        "mask": "255.255.255.0",
        "ip": "192.168.1.2",

        "devices_list_location": "../../data/devices.json",
        "backup_location": "../../data/backup.json",

        "deamon_active": False,
        "save_delay": 5
    }
    saver().save_setup(setup)

    devices = [
            {
                "name": "device1",
                "ip": "192.168.1.3",
                "mac": "00:00:00:00:00:01"
            },
            {
                "name": "device2",
                "ip": "192.168.1.4",
                "mac": "00:00:00:00:00:02"
            }
        ]
    saver().save_devices(devices)
