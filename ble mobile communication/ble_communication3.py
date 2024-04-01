import bluetooth

def receiveMessages():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 2
    server_sock.bind(("", port))
    server_sock.listen(1)

    client_sock, address = server_sock.accept()
    print("Accepted connection from " + str(address))

    data = client_sock.recv(1024)
    print("Received [%s]" % data)

    client_sock.close()
    server_sock.close()

# Run the Bluetooth server to receive messages
receiveMessages()
