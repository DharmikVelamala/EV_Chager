import subprocess

class psti:
    def what_wifi(self):
        process = subprocess.run(['nmcli', '-t', '-f', 'ACTIVE,SSID', 'dev', 'wifi'], stdout=subprocess.PIPE)
        
        if process.returncode == 0:
            a = process.stdout.decode('utf-8').strip().split('yes:')[1]
            b = a.split("\n")[0]
            return b
        else:
            return ''

    def is_connected_to(self, ssid: str):
        current_ssid = self.what_wifi()
        if current_ssid == ssid:
            return 4
        else:
            return 0
            
    def scan_wifi(self):
        process = subprocess.run(['nmcli', '-t', '-f', 'SSID,SECURITY,SIGNAL', 'dev', 'wifi'], stdout=subprocess.PIPE)
        if process.returncode == 0:
            return process.stdout.decode('utf-8').strip().split('\n')
        else:
            return []
            
    def is_wifi_available(self, ssid: str):
        return ssid in [x.split(':')[0] for x in self.scan_wifi()]

    def connect_to(self, ssid: str, password: str):
        if not self.is_wifi_available(ssid):
            return False
        subprocess.call(['nmcli', 'd', 'wifi', 'connect', ssid, 'password', password])
        return self.is_connected_to(ssid)

    def connect_to_saved(self, ssid: str):
        if not self.is_wifi_available(ssid):
            return False
        subprocess.call(['nmcli', 'c', 'up', ssid])
        return self.is_connected_to(ssid)

"""a=psti().connect_to("PSTI","psti@123")
print(a)"""
