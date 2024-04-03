import bluepy.btle as btle
import time

# Create a BLE peripheral
peripheral = btle.Peripheral()

# Define standard Bluetooth SIG UUIDs for the Device Name characteristic
device_name_char_uuid = btle.UUID("00002a00-0000-1000-8000-00805f9b34fb")

# Create a new service for GAP
gap_service = btle.Service()
gap_service.setAssignedNumber(btle.UUID("00001800-0000-1000-8000-00805f9b34fb"))

# Create a new characteristic for Device Name within the GAP service
device_name_char = gap_service.addCharacteristic(device_name_char_uuid, btle.Characteristic.READ)
device_name_char.set_value("RaspberryPi_BLE")

# Add the GAP service to the peripheral
peripheral.add_service(gap_service)

# Start advertising as a BLE peripheral
peripheral.advertise(btle.AdvertisingData(
    btle.AdvertisingFlags.general_discoverable | btle.AdvertisingFlags.br_edr_not_supported,
    name="RaspberryPi_BLE"
))

print("Advertising as 'RaspberryPi_BLE'...")

try:
    # Keep advertising for a specified duration (e.g., 30 seconds)
    time.sleep(30)
finally:
    # Stop advertising and clean up
    peripheral.stop_advertising()
    peripheral.disconnect()
