import subprocess

def connect_to_wifi(ssid, password):
    try:
        # Generate the network configuration for wpa_supplicant
        network_config = f'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev \ncountry=IN\nupdate_config=1\n network={{\n  ssid="{ssid}"\n  psk="{password}"\n  scan_ssid=1\n}}'

        # Write the network configuration to a temporary file
        with open('/tmp/wpa_supplicant.conf', 'w') as config_file:
            config_file.write(network_config)

        # Move the temporary file to the wpa_supplicant directory
        subprocess.check_call(['sudo', 'mv', '/tmp/wpa_supplicant.conf', '/etc/wpa_supplicant/wpa_supplicant.conf'])

        # Restart the wpa_supplicant service
        subprocess.check_call(['sudo', 'systemctl', 'restart', 'wpa_supplicant'])

        print(f"Connected to WiFi network: {ssid}")
    except subprocess.CalledProcessError as e:
        print(f"Error connecting to WiFi network: {e}")

# Replace 'YourWiFiSSID' and 'YourWiFiPassword' with your actual WiFi credentials
wifi_ssid = 'PSTI'
wifi_password = 'psti@123'

connect_to_wifi(wifi_ssid, wifi_password)
