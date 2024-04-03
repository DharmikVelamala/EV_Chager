from fastapi import FastAPI
from bluetooth import BluetoothSocket, RFCOMM
import subprocess

app = FastAPI()

# Function to connect to WiFi
def connect_to_wifi(ssid, password):
    try:
        network_config = f'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev \ncountry=IN\nupdate_config=1\n network={{ssid="{ssid}"\n psk="{password}"\n scan_ssid=1}}'

        with open('/tmp/wpa_supplicant.conf', 'w') as config_file:
            config_file.write(network_config)

        subprocess.check_call(['sudo', 'mv', '/tmp/wpa_supplicant.conf', '/etc/wpa_supplicant/wpa_supplicant.conf'])
        subprocess.check_call(['sudo', 'systemctl', 'restart', 'wpa_supplicant'])

        print(f"Connected to WiFi network: {ssid}")
    except subprocess.CalledProcessError as e:
        print(f"Error connecting to WiFi network: {e}")

# Function to receive messages via Bluetooth
def receiveMessages():
    server_sock = BluetoothSocket(RFCOMM)
    port = 2
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

            # Connect to WiFi if credentials are received
            if len(data.decode('utf-8').split()) == 2:
                connect_to_wifi(*data.decode('utf-8').split())

    except Exception as e:
        print("Bluetooth connection error:", e)

    finally:
        client_sock.close()
        server_sock.close()

# Start the Bluetooth server
receiveMessages()

# Define the API
app = FastAPI()

@app.post("/connect_wifi/")
async def connect_wifi(ssid: str, password: str):
    connect_to_wifi(ssid, password)
    return {"message": "Connected to WiFi"}

@app.post("/send_data/")
async def send_data(data: str):
    # Implement logic to send data via Bluetooth
    print("Received data:", data)
    return {"message": "Data received"}