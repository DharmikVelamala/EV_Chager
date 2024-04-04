import bluetooth

def start_bluetooth_server(allowed_mac_address):
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]
    print(f"Waiting for connection on RFCOMM channel {port}")

    while True:
        client_sock, client_info = server_sock.accept()
        print(f"Accepted connection from {client_info}")
        
        # Check if the client's MAC address matches the allowed MAC address
        if client_info[0] != allowed_mac_address:
            print("Unauthorized client. Closing connection.")
            client_sock.close()
            continue

        try:
            while True:
                data = client_sock.recv(1024)
                if not data:
                    break
                print(f"Received data: {data.decode('utf-8')}")

        except bluetooth.btcommon.BluetoothError as e:
            print("Bluetooth connection error:", e)

        finally:
            client_sock.close()

if __name__ == "__main__":
    allowed_mac_address = '3C:A2:C3:6B:9C:E9'  # Replace with the allowed MAC address
    start_bluetooth_server(allowed_mac_address)