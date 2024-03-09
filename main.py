# main.py

from BluetoothLocator import BluetoothLocator

def main():
    locator = BluetoothLocator()
    device_address = '00:1A:7D:DA:71:13'  # Example Bluetooth device address
    rssi = locator.fetch_rssi(device_address)
    print(f"The RSSI for device {device_address} is {rssi}")

if __name__ == "__main__":
    main()
