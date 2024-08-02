from bluepy import bluepy as b
from b import btle
def get_rssi_values(target_addresses, scan_time=10):
    scanner = btle.Scanner()
    devices = scanner.scan(scan_time)
    
    rssi_values = {}
    for device in devices:
        if device.addr in target_addresses:
            rssi_values[device.addr] = device.rssi
    
    return rssi_values

if __name__ == "__main__":
    BT_ADDR_LIST = ["3C:A2:C3:6B:9C:E9", "00:1A:7D:DA:71:13"]  # Replace with your target MAC addresses
    scan_duration = 10  # Scan duration in seconds
    
    rssi_results = get_rssi_values(BT_ADDR_LIST, scan_duration)
    
    for addr, rssi in rssi_results.items():
        print(f"MAC Address: {addr}, RSSI: {rssi} dBm")
