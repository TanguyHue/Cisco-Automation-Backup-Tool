from json import load


def set_save(backup_location, devices_file):
    mac_address = backup_location.split('/')[-2].replace("-", ":")
    devices_list = load(open(devices_file, "r"))
    
    for device in devices_list:
        if device['mac'] == mac_address:
            device_info = device

    device = {
        'device_type': device_info["type"],
        'ip': device_info["ip"],
        'username': device_info["username"], 
        'password': device_info["password"], 
        'secret': device_info["enable_password"]
    }

    try:
        with open(backup_location, 'r') as f:
            #net_connect = netmiko.ConnectHandler(**device)
            #net_connect.enable()
            #for command in f:
            #    output = net_connect.send_config_set(command)
            #    print(output)
            #net_connect.disconnect()
            print(f"Configuration of {device_info['mac']} done")
    except FileExistsError:
        print("File not found")