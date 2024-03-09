# main.py

from BluetoothLocator import BluetoothLocator

def main():
    locator = BluetoothLocator()
    locator.scan_for_devices()

    # locator.scan_devices()
    # print("The scanned devices are: ", locator.devices)
    # n_device = 0
    # if len(locator.devices) > 0:
    #     print("Using the corresponding number, select desired device to connect to.")
    #     for key, value in locator.devices.items():
    #         print(str(n_device) +"\t" + key + "\t" + value)
    #         n_device += 1
    #     user_selection = input("Device #: ")

    #     try:
    #         int_selection = int(user_selection)
    #         if not (0 <= int_selection < n_device):
    #             print("Invalid selection, terminating.")
    #             exit()
            
    #         # MAC address of chosen device
    #         for i, (key, value) in enumerate(locator.devices.items()):
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
