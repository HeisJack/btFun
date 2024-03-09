from bluepy.btle import Scanner
import dbus
import subprocess
import threading
import time

class BluetoothLocator:
    def __init__(self):
        self.devices = {}

    def scan_for_devices(self):
        scanner = Scanner()
        devices = scanner.scan(10.0)

        for device in devices:
            print(f"Device {device.addr} ({device.addrType}), RSSI={device.rssi} dB")


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
    
    def print_scanning_message(self, stop_event):
        dot_count = 0
        while not stop_event.is_set():
            print(f'\rScanning for devices{"." * dot_count}', end ='')
            dot_count += 1
            time.sleep(1)
        print()
        
    def scan_devices(self):
        """
        Scans for Bluetooth devices using hcitool and returns a list of tuples containing MAC addresses and device names.
        """
        stop_message = threading.Event()
        message_thread = threading.Thread(target=self.print_scanning_message, args=(stop_message,))
        message_thread.start()

        try:
            scan_output = subprocess.check_output(['hcitool', 'scan'], encoding='utf-8')
            # Process the output to extract device information
            lines = scan_output.split('\n')[1:]  # First line is the header, so skip it
            for line in lines:
                parts = line.split('\t')
                if len(parts) >= 2:
                    mac_address = parts[1]
                    name = parts[2]
                    self.devices[name] = mac_address
        except subprocess.CalledProcessError as e:
            print(f"Failed to scan Bluetooth devices: {e}")
        
        stop_message.set()
        message_thread.join()
