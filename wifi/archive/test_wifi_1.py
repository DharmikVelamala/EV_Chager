import wifi_1
# Unit test with mocked subprocess calls
import pytest
@pytest.mark.usefixtures("mocked_subprocess_run")
def test_connect_to_success(mocked_subprocess_run):
  # Mock successful nmcli calls
  mocked_subprocess_run.side_effect = [
      # Mock what_wifi to return a specific SSID
      subprocess.CompletedProcess(['nmcli', '-t', '-f', 'ACTIVE,SSID', 'dev', 'wifi'], returncode=0, stdout=b'ACTIVE:yes\nSSID:my_test_ssid'),
      # Mock successful connection
      subprocess.CompletedProcess(['nmcli', 'd', 'wifi', 'connect', 'my_test_ssid', 'password', 'test_password'], returncode=0)
  ]

  # Call connect_to with mocked SSID and password
  assert connect_to("my_test_ssid", "test_password") is True

# Fixture to mock subprocess.run calls
@pytest.fixture
def mocked_subprocess_run(mocker):
  return mocker.patch("subprocess.run")