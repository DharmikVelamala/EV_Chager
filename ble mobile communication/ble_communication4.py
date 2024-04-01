import bluetooth

def receiveMessages():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1
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

    except bluetooth.btcommon.BluetoothError as e:
        print("Bluetooth connection error:", e)

    finally:
        client_sock.close()
        server_sock.close()

# Run the Bluetooth server to receive messages
receiveMessages()
