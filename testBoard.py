#Test script to check and calibrate board functionality

import serial
import time
ser = serial.Serial('/dev/cu.usbserial-0001', 115200, timeout=1)

while True:
    ser.write(b"ON")
    time.sleep(3)
    