import bluetooth

# Bluetooth server setup
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 1  # RFCOMM port number

server_sock.bind(("", port))
server_sock.listen(1)

print("Waiting for connection...")

# Accept incoming connection
client_sock, client_info = server_sock.accept()
print("Accepted connection from", client_info)

# Receive data from client (mobile device)
data = client_sock.recv(1024).decode()
print("Received data:", data)

# Process the received data and generate a response message
# For simplicity, assume the data contains device PIN and user ID
device_pin, user_id = data.split(';')
response_message = f"Received Device PIN: {device_pin}, User ID: {user_id}"
print("Response:", response_message)

# Send the response message back to the client
client_sock.send(response_message.encode())

# Close the connection
client_sock.close()
server_sock.close()
