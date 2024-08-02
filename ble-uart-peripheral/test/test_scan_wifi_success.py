import unittest
from unittest.mock import patch,MagicMock
from wifi_2 import psti

class TestWifi(unittest.TestCase):

    @patch('wifi_2.subprocess.run')
    def test_scan_wifi_success(self, mock_subprocess_run):
        # Set up
        mock_subprocess_run.return_value = MagicMock(returncode=0, stdout=b'SSID1:WPA;TKIP;CCMP\nSSID2:WPA;TKIP;CCMP\n')
        
        # Instantiate psti object
        obj = psti()

        # Call the method under test
        result = obj.scan_wifi()

        # Assertions
        self.assertIsInstance(result, list)  # Verify the result is a list
        for network in result:
            self.assertIsInstance(network, dict)  # Verify each item in the list is a dictionary
            self.assertIn('SSID', network)  # Verify each network dictionary contains SSID key
            self.assertIn('SECURITY', network)  # Verify each network dictionary contains SECURITY key
            self.assertIn('SIGNAL', network)  # Verify each network dictionary contains SIGNAL key

if __name__ == '__main__':
    unittest.main()
