
import bluetooth

def receiveMessages(targetBluetoothMacAddress):
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 2
    server_sock.bind(("", port))
    server_sock.listen(1)
    print(22)
    client_sock, address = server_sock.accept()
    print("Accepted connection from " + str(address))
    print(34)

    data = client_sock.recv(1024)
    print("Received [%s]" % data)
    if data:
        client_sock.close()
        server_sock.close()

def sendMessageTo(targetBluetoothMacAddress):
    port = 2
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    print(1)
    sock.connect((targetBluetoothMacAddress, port))
    print(20)
    sock.send("hello!!")
    print(30)
    sock.close()

def lookUpNearbyBluetoothDevices(targetMacAddress):
    nearby_devices = bluetooth.discover_devices()
    for bdaddr in nearby_devices:
        print(str(bluetooth.lookup_name(bdaddr)) + " [" + str(bdaddr) + "]")
        if bdaddr == targetMacAddress:
            print(1)
            sendMessageTo(targetMacAddress)

# Replace '3C:A2:C3:6B:9C:E9' with the MAC address of the target Bluetooth device
targetMacAddress = "3C:A2:C3:6B:9C:E9"
lookUpNearbyBluetoothDevices(targetMacAddress)