import re
# main.py

from BluetoothLocator import BluetoothLocator

def is_valid_mac_address(mac):
    pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
    return bool(pattern.match(mac))

def main():
    locator = BluetoothLocator()
    # locator.scan_ble_devices()
    # locator.scan_devices()

    locator.run_in_parallel(locator.scan_devices, locator.robust_scan) # calls the scan_devices() and scan_ble_devices() functions and runs them in parallel
    print("The scanned devices are: ", locator.hci_devices)
    print("The scanned ble devices are: ", locator.ble_devices)
    locator.resolve_mac_addresses()
    
    
    n_device = 0
    if(len(locator.unified_dict)) > 0:
        print("\nUsing the corresponding number, select desired device to connect to:")
        print("\n")
        print("Selector\t" + "MAC\t" + "Address Type\t" + "RSSI(db)\t" + "Name")
        for key, value in locator.unified_dict.items():
            output_string = str(key) + "\t"
            for key2, value2 in value.items():
                output_string = output_string + str(value2) + "\t"
            print(output_string)
            output_string = ""
        user_selection = input("Provide a device Selector # or type 'Other' to attempt to connect to another device: ")
        
        mac_selection = ""
        if str(user_selection).lower() != 'other':
            try:
                int_selection = int(user_selection)
                if not (0 <= int_selection < len(locator.unified_dict)):
                    print("Invalid selection, terminating.")
                    exit()
            except ValueError:
                print("Please input a valid integer value corresponding to the device you wish to connect to.")
            
            mac_selection = locator.unified_dict[user_selection]['mac']

        else:
            mac_selection = input("Please provide another MAC in the format of XX:XX:XX:XX:XX:XX \n")
            mac_selection = mac_selection.lower()
            if is_valid_mac_address(mac_selection):
                print("Provided MAC address: ", mac_selection)

            else:
                print("Invalid MAC input, please ensure MAC is in format of XX:XX:XX:XX:XX:XX:XX\nExiting...")
                exit()
        
        print("This is the MAC address you selected: ", mac_selection)

        rssi = locator.unified_dict[user_selection]['RSSI']
        tx_power = -46
        path_loss_exponent = 2 # indoor environment will typically have between 2 and 4 for this value

        offset_dist = locator.rssi_to_distance(rssi, tx_power, path_loss_exponent)
        print(f"This device is approx. {str(offset_dist)} away")



    else:
        print("No BT devices detected, exiting.")
        exit()



    # if len(locator.hci_devices) > 0:
    #     print("Using the corresponding number, select desired device to connect to.")
    #     for key, value in locator.hci_devices.items():
    #         print(str(n_device) +"\t" + key + "\t" + value)
    #         n_device += 1
    #     user_selection = input("Device #: ")

    #     try:
    #         int_selection = int(user_selection)
    #         if not (0 <= int_selection < n_device):
    #             print("Invalid selection, terminating.")
    #             exit()
            
    #         # MAC address of chosen device
    #         for i, (key, value) in enumerate(locator.hci_devices.items()):
    #             if i == int_selection:
    #                 print("True, int_selection: ", int_selection)
    #                 print("device_address: ", value)
    #                 device_address = value
    #             rssi = locator.get_rssi(device_address)
    #             print(f"The RSSI for device {device_address} is {rssi}")
    #     except ValueError:
    #         print("Please input a valid integer value corresponding to the device you wish to connect to.")


    # device_address = '00:1A:7D:DA:71:13'  # Example Bluetooth device address
    # rssi = locator.fetch_rssi(device_address)
    # print(f"The RSSI for device {device_address} is {rssi}")

if __name__ == "__main__":
    main()
