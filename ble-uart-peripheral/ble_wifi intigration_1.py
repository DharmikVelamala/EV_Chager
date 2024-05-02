import sys
import dbus, dbus.mainloop.glib
from gi.repository import GLib
from example_advertisement import Advertisement
from example_advertisement import register_ad_cb, register_ad_error_cb
from example_gatt_server import Service, Characteristic
from example_gatt_server import register_app_cb, register_app_error_cb
import subprocess
from wifi import psti

BLUEZ_SERVICE_NAME =           'org.bluez'
DBUS_OM_IFACE =                'org.freedesktop.DBus.ObjectManager'
LE_ADVERTISING_MANAGER_IFACE = 'org.bluez.LEAdvertisingManager1'
GATT_MANAGER_IFACE =           'org.bluez.GattManager1'
GATT_CHRC_IFACE =              'org.bluez.GattCharacteristic1'
UART_SERVICE_UUID =            '6e400001-b5a3-f393-e0a9-e50e24dcca9e'
UART_RX_CHARACTERISTIC_UUID =  '6e400002-b5a3-f393-e0a9-e50e24dcca9e'
UART_TX_CHARACTERISTIC_UUID =  '6e400003-b5a3-f393-e0a9-e50e24dcca9e'
LOCAL_NAME =                   'rpi-gatt-server'
mainloop = None
a=[]
Wifi=psti()

class TxCharacteristic(Characteristic):
    def __init__(self, bus, index, service):
        Characteristic.__init__(self, bus, index, UART_TX_CHARACTERISTIC_UUID,
                                ['notify'], service)
        self.notifying = False
        GLib.io_add_watch(sys.stdin, GLib.IO_IN, self.on_console_input)

    def on_console_input(self, fd, condition):
        s = fd.readline()
        if s.isspace():
            pass
        else:
            self.send_tx(s)
        return True

    def send_tx(self, s):
        if not self.notifying:
            return
        value = []
        for c in s:
            value.append(dbus.Byte(c.encode()))
        self.PropertiesChanged(GATT_CHRC_IFACE, {'Value': value}, [])

    def StartNotify(self):
        if self.notifying:
            return
        self.notifying = True

    def StopNotify(self):
        if not self.notifying:
            return
        self.notifying = False

class RxCharacteristic(Characteristic):
    def __init__(self, bus, index, service):
        Characteristic.__init__(self, bus, index, UART_RX_CHARACTERISTIC_UUID,
                                ['write'], service)

    def WriteValue(self, value, options):
        
        #print('remote: {}'.format(bytearray(value).decode()))
        data = bytearray(value).decode()
        print('Received: {}'.format(data))
        a.append(data)
        # Store received data in a file with specific format
        with open('received_data.txt', 'a') as file:
            file.write(data + '\n')
        if len(a)==17:
        # Process and extract information from the received data
            process_received_data(a)
        
        

def process_received_data(data):
    # Split the data into individual fields
    #fields = data.split(';')
    fields=a
    #print(fields)
    # Extract information from the fields
    device_pin = fields[0]
    user_id = fields[1]
    user_rights = fields[2]
    user_name = fields[3]
    user_email = fields[4]
    device_mac = fields[5]
    vehicle_manufacturer = fields[6]
    vehicle_model = fields[7]
    vehicle_class = fields[8]
    vehicle_variant = fields[9]
    vehicle_color = fields[10]
    wifi_ssid = fields[11]
    wifi_password = fields[12]
    timestamp = fields[13]
    battery_capacity = fields[14]
    vehicle_image = fields[15]
    efficiency_mileage = fields[16]
    
    wifi_flag=Wifi.connect_to(wifi_ssid.split("\r")[0],wifi_password.split("\r")[0])
    print(wifi_flag)
    a.clear()
    # Format the information and store it in a specific format
    formatted_data = f"Device PIN: {device_pin}\n" \
                     f"User ID: {user_id}\n" \
                     f"User Rights: {user_rights}\n" \
                     f"User Name: {user_name}\n" \
                     f"User Email: {user_email}\n" \
                     f"Device MAC Address: {device_mac}\n" \
                     f"Vehicle Manufacturer: {vehicle_manufacturer}\n" \
                     f"Vehicle Model: {vehicle_model}\n" \
                     f"Vehicle Class: {vehicle_class}\n" \
                     f"Vehicle Variant: {vehicle_variant}\n" \
                     f"Vehicle Color: {vehicle_color}\n" \
                     f"Wi-Fi SSID: {wifi_ssid}\n" \
                     f"Wi-Fi Password: {wifi_password}\n" \
                     f"Timestamp: {timestamp}\n" \
                     f"Battery Capacity: {battery_capacity}\n" \
                     f"Vehicle Image: {vehicle_image}\n" \
                     f"Efficiency/Mileage: {efficiency_mileage}\n"
    
    # Store the formatted data in a separate file
    with open('formatted_data.txt', 'a') as file:
        file.write(formatted_data + '\n')
        
    return wifi_flag
		


        

class UartService(Service):
    def __init__(self, bus, index):
        Service.__init__(self, bus, index, UART_SERVICE_UUID, True)
        self.add_characteristic(TxCharacteristic(bus, 0, self))
        self.add_characteristic(RxCharacteristic(bus, 1, self))

class Application(dbus.service.Object):
    def __init__(self, bus):
        self.path = '/'
        self.services = []
        dbus.service.Object.__init__(self, bus, self.path)

    def get_path(self):
        return dbus.ObjectPath(self.path)

    def add_service(self, service):
        self.services.append(service)

    @dbus.service.method(DBUS_OM_IFACE, out_signature='a{oa{sa{sv}}}')
    def GetManagedObjects(self):
        response = {}
        for service in self.services:
            response[service.get_path()] = service.get_properties()
            chrcs = service.get_characteristics()
            for chrc in chrcs:
                response[chrc.get_path()] = chrc.get_properties()
        return response

class UartApplication(Application):
    def __init__(self, bus):
        Application.__init__(self, bus)
        self.add_service(UartService(bus, 0))

class UartAdvertisement(Advertisement):
    def __init__(self, bus, index):
        Advertisement.__init__(self, bus, index, 'peripheral')
        self.add_service_uuid(UART_SERVICE_UUID)
        self.add_local_name(LOCAL_NAME)
        self.include_tx_power = True

def find_adapter(bus):
    remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'),
                               DBUS_OM_IFACE)
    objects = remote_om.GetManagedObjects()
    for o, props in objects.items():
        if LE_ADVERTISING_MANAGER_IFACE in props and GATT_MANAGER_IFACE in props:
            return o
        print('Skip adapter:', o)
    return None

def main():
    global mainloop
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    adapter = find_adapter(bus)
    if not adapter:
        print('BLE adapter not found')
        return

    service_manager = dbus.Interface(
                                bus.get_object(BLUEZ_SERVICE_NAME, adapter),
                                GATT_MANAGER_IFACE)
    ad_manager = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, adapter),
                                LE_ADVERTISING_MANAGER_IFACE)

    app = UartApplication(bus)
    adv = UartAdvertisement(bus, 0)

    mainloop = GLib.MainLoop()

    service_manager.RegisterApplication(app.get_path(), {},
                                        reply_handler=register_app_cb,
                                        error_handler=register_app_error_cb)
    ad_manager.RegisterAdvertisement(adv.get_path(), {},
                                     reply_handler=register_ad_cb,
                                     error_handler=register_ad_error_cb)
    try:
        mainloop.run()
    except KeyboardInterrupt:
        adv.Release()

if __name__ == '__main__':
    main()
