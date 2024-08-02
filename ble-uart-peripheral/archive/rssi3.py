import asyncio
from bleak import BleakScanner

import bluepy.btle as btle
import time
target_addresses = ["3C:A2:C3:6B:9C:E9", "17:7C:2B:CA:A5:B2","AC:C0:48:9E:33:1E"]

# Replace with your device's address
device_address = "3C:A2:C3:6B:9C:E9"

# Create a Bluetooth adapter
adapter = btle.Adapter()

# Set up the device
device = btle.Peripheral(adapter, device_address)

while True:
    # Get the RSSI value
    rssi = device.get_rssi()
    print(f"RSSI: {rssi}")
    time.sleep(1)  # Wait for 1 second before checking again
