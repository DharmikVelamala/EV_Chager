import pytest
import subprocess

def test_connect_to_wifi():
    # Mock the subprocess.check_call function
    with patch('subprocess.check_call') as mock_check_call:
        # Call the function to connect to the WiFi network
        connect_to_wifi('Pty', 'psti@123')

        # Check if the mocks were called with the expected arguments
        mock_check_call.assert_any_call(['sudo', 'mv', '/tmp/wpa_supplicant.conf', '/etc/wpa_supplicant/wpa_supplicant.conf'])
        mock_check_call.assert_any_call(['sudo', 'systemctl', 'restart', 'wpa_supplicant'])

        # Check if the function printed the expected message
        assert "Connected to WiFi network: PSTI" in subprocess.check_output("echo $PRINT", shell=True).decode()

def test_connect_to_wifi_error():
    # Mock the subprocess.check_call function
    with patch('subprocess.check_call') as mock_check_call:
        # Mock the subprocess.CalledProcessError exception
        mock_check_call.side_effect = subprocess.CalledProcessError(1, "wpa_supplicant")

        # Call the function to connect to the WiFi network
        with pytest.raises(subprocess.CalledProcessError):
            connect_to_wifi('PS', 'psti@123')

        # Check if the mocks were called with the expected arguments
        mock_check_call.assert_any_call(['sudo', 'mv', '/tmp/wpa_supplicant.conf', '/etc/wpa_supplicant/wpa_supplicant.conf'])
        mock_check_call.assert_any_call(['sudo', 'systemctl', 'restart', 'wpa_supplicant'])

        # Check if the function printed the expected error message
        assert "Error connecting to WiFi network: Command '['sudo', 'systemctl', 'restart', 'wpa_supplicant']' returned non-zero exit status 1" in subprocess.check_output("echo $PRINT", shell=True).decode()