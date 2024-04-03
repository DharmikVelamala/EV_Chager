from bt_proximity import BluetoothRSSI
import time
import bluetooth
import subprocess

# List of Bluetooth addresses to scan
BT_ADDR_LIST = ["3C:A2:C3:6B:9C:E9"]
wifi_credentials = []
DEBUG=True
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
    port = 2
    server_sock.bind(("", port))
    server_sock.listen(1)
    try:
        
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
    while True:
        rssi = b.request_rssi()
        if debug:
            print("addr: {}, rssi: {}".format(addr, rssi))
        # Sleep and then skip to next iteration if device not found
        if rssi is None:
            time.sleep(1)
            continue
        # Trigger if RSSI value is within threshold
        if threshold[0] < rssi[0] < threshold[1]:
            receiveMessages()
        # Delay between iterations
        time.sleep(1)

def main():
    for addr in BT_ADDR_LIST:
        bluetooth_listen(addr,THRESHOLD,DEBUG)

if __name__ == '__main__':
    main()
