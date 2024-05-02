
ssid = "psti"
password = "psti"

network_config = f'country=IN\nupdate_config=1\nctrl_interface=/var/run/wpa_supplicant\nnetwork={{\n scan_ssid=1 \n ssid="{ssid}"\n  psk="{password}"\n}}'
