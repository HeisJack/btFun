import dbus

class BluetoothLocator:
    def __init__(self):
        pass

    def get_rssi(self, device_address):
        # D-Bus object paths
        bus = dbus.SystemBus()
        adapter_path = '/org/bluez/hci0'  # Adjust if using a different adapter
        device_path = f'{adapter_path}/dev_{device_address.replace(":", "_")}'

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
