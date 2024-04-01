from bt_proximity import BluetoothRSSI
import time
import bluetooth
import subprocess
from bt_proximity import BluetoothRSSI
import datetime
import threading
import sys

# List of Bluetooth addresses to scan
BT_ADDR_LIST = []
wifi_credentials = []
duration = 10
DEBUG=False
THRESHOLD = (-1, 20)

def connect_to_wifi(ssid, password):
    try:
        # Generate the network configuration for wpa_supplicant
        network_config = f'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev \ncountry=IN\nupdate_config=1\n network={{\n  ssid="{ssid}"\n  psk="{password}"\n  scan_ssid=1\n}}'

        # Write the network configuration to a temporary file
        with open('/tmp/wpa_supplicant.conf', 'w') as config_file:
            config_file.write(network_config)

        # Move the temporary file to the wpa_supplicant directory
        subprocess.check_call(['sudo', 'mv', '/tmp/wpa_supplicant.conf', '/etc/wpa_supplicant/wpa_supplicant.conf'])

        # Restart the wpa_supplicant service
        subprocess.check_call(['sudo', 'systemctl', 'restart', 'wpa_supplicant'])

        print(f"Connected to WiFi network: {ssid}")
    except subprocess.CalledProcessError as e:
        print(f"Error connecting to WiFi network: {e}")

def receiveMessages():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1
    try:
        server_sock.bind(("", port))
        server_sock.listen(1)
        print("Waiting for connection on RFCOMM channel %d" % port)

        client_sock, client_info = server_sock.accept()
        print("Accepted connection from", client_info)
        Data=" "
        try:
            # Flag to track if a successful connection has been made
            while True:
                data = client_sock.recv(1024)
                if not data:
                    break
                print("Received:", data.decode('utf-8'))
                Data+=data.decode('utf-8')
                wifi_credentials=Data.split()
                if len(wifi_credentials) == 2:
                    print("Sending data after successful connection")
                    connect_to_wifi(wifi_credentials[0], wifi_credentials[1])
                    Data=" "
                    
        except bluetooth.btcommon.BluetoothError as e:
            print("Bluetooth connection error:", e)
        finally:
            client_sock.close()
    except bluetooth.btcommon.BluetoothError as e:
        print("Bluetooth socket error:", e)
    finally:
        server_sock.close()

def bluetooth_listen(addr, threshold,debug):
    b = BluetoothRSSI(addr=addr)
#     while True:
    rssi = b.request_rssi()
    if debug:
        print("addr: {}, rssi: {}".format(addr, rssi))
    # Sleep and then skip to next iteration if device not found
    if rssi is None:
        return
    # Trigger if RSSI value is within threshold
    if threshold[0] < rssi[0] < threshold[1]:
        receiveMessages()
    # Delay between iterations
    time.sleep(1)
    
    
def start_thread(addr, threshold=THRESHOLD,debug=DEBUG):
    """Helper function that creates and starts a thread to listen for the
    bluetooth address.

    @param: addr: Bluetooth address
    @type: addr: str

    @param: callback: Function to call when RSSI is within threshold
    @param: callback: function

    @param: threshold: Tuple of the high/low RSSI value to trigger callback
    @type: threshold: tuple of int

    @param: sleep: Time in seconds between RSSI scans
    @type: sleep: int or float

    @param: daily: Daily flag to pass to `bluetooth_listen` function
    @type: daily: bool

    @param: debug: Debug flag to pass to `bluetooth_listen` function
    @type: debug: bool

    @return: Python thread object
    @rtype: threading.Thread
    """
    thread = threading.Thread(
        target=bluetooth_listen,
        args=(),
        kwargs={
            'addr': addr,
            'threshold': threshold,
            'debug': debug
        }
    )
    # Daemonize
    thread.daemon = True
    # Start the thread
    thread.start()
    return thread


    
    
    
    
    

def main():
#     start=time.time()
#     while time.time()-start<=duration:
    BT_ADDR_LIST = bluetooth.discover_devices(duration=duration, lookup_names=False)   
        
    threads = []
    for addr in BT_ADDR_LIST:
#         print(addr)
        th = start_thread(addr=addr)
        threads.append(th)
    while True:
        # Keep main thread alive
        time.sleep(1)
        
        
if __name__ == '__main__':
    main()

