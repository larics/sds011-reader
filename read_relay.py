#!/usr/bin/python3
"""
Script for testing datareyaling through tty
"""


import serial, datetime, time
import os

from datetime import date, datetime

ser = serial.Serial('/dev/ttyUSB2')

print("Connected to " + ser.port)

print("h, min, sec, id, pm_25, pm_10")

while True:
    print("Waiting for data:")
    data = []
    for index in range(0, 10):
        datum = ser.read()
        data.append(datum)

    pm_25 = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
    pm_10 = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10

    sensor_id = int.from_bytes(b''.join(data[6:8]), byteorder='little')

    now = datetime.now()
    output_string = str(now.hour) + ', ' + str(now.minute) + ', ' \
                    + str(now.second) + ', ' + str(sensor_id) + ', ' \
                    + str(pm_25) + ', ' + str(pm_10) + '\n'

    print(output_string)
    time.sleep(0.95)
