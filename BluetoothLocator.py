from bluepy.btle import Scanner, BTLEException
import dbus
import subprocess
import threading
import concurrent.futures
import math

class BluetoothLocator:
    def __init__(self):
        self.hci_devices = []
        self.ble_devices = []

        self.unified_dict = {}


    def scan_ble_devices(self):
        scanner = Scanner()
        scan_devices = scanner.scan(10.0)

        for device in scan_devices:
            print(f"Device {device.addr} ({device.addrType}), RSSI={device.rssi} dB")
            device_dict = {
                "mac": device.addr,
                "addressType": device.addrType,
                "RSSI": device.rssi
            }
            self.ble_devices.append(device_dict)

    def robust_scan(self):
        max_attempts = 3
        attempts = 0
        while attempts < max_attempts:
            try:
                return self.scan_ble_devices()
            except BTLEException as e:
                attempts += 1
                print("Retrying scan due to exception: {e}")


    def resolve_mac_addresses(self):

        if len(self.hci_devices) < 1 or len(self.ble_devices) < 1:
            print("There is not enough scan data to perform device resolution.")
            return

        list_copy = self.ble_devices.copy()
        temp_list = []

        for dictionary1 in self.hci_devices:
            match = False
            for dictionary2 in list_copy:
                if dictionary1['mac'] == dictionary2['mac']:
                    match =True
                    dictionary2['name'] = dictionary1['name']
            if not match:
                dict_copy = dictionary1.copy()
                dict_copy['RSSI'] = 'n/a'
                dict_copy['addressType'] = 'n/a'
                temp_list.append(dict_copy)
        
        for item in temp_list:
            list_copy.append(item)
        
        for dictionary in list_copy:
            if 'name' not in dictionary:
                dictionary['name'] = 'n/a'
        
        temp_dict = {}
        index = 0
        for dictionary in list_copy:
            dict_copy = dictionary.copy()
            temp_key = str(index)
            temp_dict[temp_key] = dict_copy
            index += 1

        self.unified_dict = temp_dict

    def rssi_to_distance(self, rssi, tx_power, path_loss_exponent):
        """
        Convert RSSI value to distance in meters.
        
        :param rssi: The RSSI value in dBm.
        :param tx_power: The calibrated RSSI value at 1 meter. Typically between -60 and -70 dBm.
        :param path_loss_exponent: The path loss exponent, depending on the environment.
        :return: The estimated distance in meters.
        """
        if rssi == 0:
            return -1.0  # distance cannot be calculated

        # Calculate the ratio of the RSSI to the Tx Power
        ratio = rssi / tx_power
        # Use the path loss exponent in the distance calculation
        distance = math.pow(10, (tx_power - rssi) / (10 * path_loss_exponent))

        return distance


    def get_rssi(self, device_address):
        # D-Bus object paths
        bus = dbus.SystemBus()
        adapter_path = '/org/bluez/hci0'  # Adjust if using a different adapter
        device_path = f'{adapter_path}/dev_{device_address.replace(":", "_")}'
        print("Device path is: ", device_path)

        # Getting the device proxy
        device_proxy = bus.get_object('org.bluez', device_path)
        device_properties = dbus.Interface(device_proxy, 'org.freedesktop.DBus.Properties')

        # Getting the RSSI value
        try:
            rssi = device_properties.Get('org.bluez.Device1', 'RSSI')
            return rssi
        except dbus.exceptions.DBusException as e:
            print(f"Error accessing device properties: {e}")
            return None
    
        
    def scan_devices(self):
        """
        Scans for Bluetooth devices using hcitool and returns a list of tuples containing MAC addresses and device names.
        """

        try:
            scan_output = subprocess.check_output(['hcitool', 'scan'], encoding='utf-8')
            # Process the output to extract device information
            lines = scan_output.split('\n')[1:]  # First line is the header, so skip it
            
            for line in lines:
                new_dict = {}
                parts = line.split('\t')
                if len(parts) >= 2:
                    new_dict['mac'] = str(parts[1]).lower()
                    new_dict['name'] = parts[2]
                    self.hci_devices.append(new_dict)
        except subprocess.CalledProcessError as e:
            print(f"Failed to scan Bluetooth devices: {e}")
    
    def run_in_parallel(*funcs):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(func) for func in funcs]
            for future in concurrent.futures.as_completed(results):
                try:
                    print("Executing HCI and BLE scans...")
                    thread_result = future.result()
                except Exception as e:
                    print(f"Generated an exception: {e}")
        


