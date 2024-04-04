# my_code.py

import RPi.GPIO as GPIO
import bluetooth
import time

LED_PIN = 18
TARGET_BLUETOOTH_ADDRESS = "3C:A2:C3:6B:9C:E9"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def detect_mobile_device():
    nearby_devices = bluetooth.discover_devices(duration=1, lookup_names=True)
    for addr, _ in nearby_devices:
        if addr == TARGET_BLUETOOTH_ADDRESS:
            return True
    return False

while True:
    if detect_mobile_device():
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("Mobile device detected. LED turned on.")
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
        print("Mobile device not detected. LED turned off.")
