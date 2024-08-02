import asyncio
from bleak import BleakScanner

# Define the set of target MAC addresses
target_addresses = ["3C:A2:C3:6B:9C:E9", "17:7C:2B:CA:A5:B2","AC:C0:48:9E:33:1E"]

async def scan_and_get_rssi():
    def detection_callback(device, advertisement_data):
        print(device.address)
        if device.address in target_addresses:
            print(f"** Target Device Found ** Device: {device.name}, Address: {device.address}, RSSI: {advertisement_data.rssi}")

    scanner = BleakScanner(detection_callback)
    #scanner = BleakScanner()
    #scanner.register_detection_callback(detection_callback)
    if True:
        await scanner.start()
        await asyncio.sleep(10)  # Scan duration
        await scanner.stop()

# Run the loop indefinitely
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(scan_and_get_rssi())
except KeyboardInterrupt:
    print("Scan stopped by user")
