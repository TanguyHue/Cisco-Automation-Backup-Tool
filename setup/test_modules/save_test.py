import sys
sys.path.append("../..")

from setup.modules.save import saver
from setup.modules.interface import interface
from setup.modules.device import device

if __name__ == "__main__":
    interface_1 = interface("eth0", "192.168.1.0", "255.255.255.0")
    saving = saver('./data_test/setup_file.json', './data_test/devices.json')
    saving.save_setup(interface_1)

    devices = [
            device("192.168.1.2", "00:00:00:00:00:02"),
            device("192.168.1.3", "00:00:00:00:00:03"),
            device("192.168.1.4", "00:00:00:00:00:04"),
        ]
    saving.save_devices(devices)
