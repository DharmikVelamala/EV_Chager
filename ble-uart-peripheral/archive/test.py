try:
    with open('mac_data.txt', 'r') as file:
        mac_content = file.read()
except FileNotFoundError:
    print("The file 'example.txt' was not found.")
except IOError:
    print("An error occurred while reading the file.")

BT_ADDR_LIST=mac_content.split("Saved bluetooth Mac address: ")[1].split("/n")[0]
print(BT_ADDR_LIST)
print(BT_ADDR_LIST)