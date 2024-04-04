
from bt_proximity import BluetoothRSSI
import datetime
import time
import threading
import sys
import bluetooth
import subprocess

# List of bluetooth addresses to scan
BT_ADDR_LIST = ["3C:A2:C3:6B:9C:E9"]
wifi_credentials=[]
DAILY = True  # Set to True to invoke callback only once per day per address
DEBUG = True  # Set to True to print out debug messages
THRESHOLD = (-1, 20)
SLEEP = 1


def dummy_callback():
    print("Dummy callback function invoked")
    
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

        try:
            while True:
                data = client_sock.recv(1024)
                if not data:
                    break
                print("Received:", data.decode('utf-8'))
                wifi_credentials.append(data.decode('utf-8'))
                if len(wifi_credentials)==2:
                    connect_to_wifi(wifi_credentials[0],wifi_credentials[1])
                    wifi_credentials.clear()
                    

        except bluetooth.btcommon.BluetoothError as e:
            print("Bluetooth connection error:", e)

        finally:
            client_sock.close()
    except bluetooth.btcommon.BluetoothError as e:
        print("Bluetooth socket error:", e)

    finally:
        server_sock.close()



def bluetooth_listen(
        addr, threshold, callback, sleep=1, daily=True, debug=False):
    """Scans for RSSI value of bluetooth address in a loop. When the value is
    within the threshold, calls the callback function.

    @param: addr: Bluetooth address
    @type: addr: str

    @param: threshold: Tuple of integer values (low, high), e.g. (-10, 10)
    @type: threshold: tuple

    @param: callback: Callback function to invoke when RSSI value is within
                      the threshold
    @type: callback: function

    @param: sleep: Number of seconds to wait between measuring RSSI
    @type: sleep: int

    @param: daily: Set to True to invoke callback only once per day
    @type: daily: bool

    @param: debug: Set to True to print out debug messages and does not 
                   actually sleep until tomorrow if `daily` is True.
    @type: debug: bool
    """
    b = BluetoothRSSI(addr=addr)
    while True:
        rssi = b.request_rssi()
        if debug:
            print("---")
            print("addr: {}, rssi: {}".format(addr, rssi))
        # Sleep and then skip to next iteration if device not found
        if rssi is None:
            time.sleep(sleep)
            continue
        # Trigger if RSSI value is within threshold
        if threshold[0] < rssi[0] < threshold[1]:
            print(1)
            receiveMessages()
            # Run the Bluetooth server to receive messages
            '''callback()
            if daily:
                # Calculate the time remaining until next day
                now = datetime.datetime.now()
                tomorrow = datetime.datetime(
                    now.year, now.month, now.day, 0, 0, 0, 0) + \
                    datetime.timedelta(days=1)
                until_tomorrow = (tomorrow - now).seconds
                if debug:
                    print("Seconds until tomorrow: {}".format(until_tomorrow))
                else:
                    time.sleep(until_tomorrow)'''
        # Delay between iterations
        time.sleep(sleep)

# 
# def start_thread(addr, callback, threshold=THRESHOLD, sleep=SLEEP,
#                  daily=DAILY, debug=DEBUG):
#     """Helper function that creates and starts a thread to listen for the
#     bluetooth address.
# 
#     @param: addr: Bluetooth address
#     @type: addr: str
# 
#     @param: callback: Function to call when RSSI is within threshold
#     @param: callback: function
# 
#     @param: threshold: Tuple of the high/low RSSI value to trigger callback
#     @type: threshold: tuple of int
# 
#     @param: sleep: Time in seconds between RSSI scans
#     @type: sleep: int or float
# 
#     @param: daily: Daily flag to pass to `bluetooth_listen` function
#     @type: daily: bool
# 
#     @param: debug: Debug flag to pass to `bluetooth_listen` function
#     @type: debug: bool
# 
#     @return: Python thread object
#     @rtype: threading.Thread
#     """
#     thread = threading.Thread(
#         target=bluetooth_listen,
#         args=(),
#         kwargs={
#             'addr': addr,
#             'threshold': threshold,
#             'callback': callback,
#             'sleep': sleep,
#             'daily': daily,
#             'debug': debug
#         }
#     )
#     # Daemonize
#     thread.daemon = True
#     # Start the thread
#     thread.start()
#     return thread


def main():
#     if not BT_ADDR_LIST:
#         print("Please edit this file and set BT_ADDR_LIST variable")
#         sys.exit(1)
#     threads = []
    for addr in BT_ADDR_LIST:
#         th = start_thread(addr=addr, callback=dummy_callback)
#         threads.append(th)
        bluetooth_listen(addr,THRESHOLD,dummy_callback)
    while True:
        # Keep main thread alive
        time.sleep(1)


if __name__ == '__main__':
    main()

