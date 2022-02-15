#!/usr/bin/python3

import serial
import time

from datetime import date, datetime

serials = [serial.Serial('/dev/ttyUSB0'),
           serial.Serial('/dev/ttyUSB1'),
           serial.Serial('/dev/ttyUSB2')]

print("Connected to /dev/ttyUSB0")
print("Connected to /dev/ttyUSB1")
print("Connected to /dev/ttyUSB2")

output_filename = "data/" + "multi_sensor" + "_" + str(date.today()) + ".csv"
print(output_filename)

output_file = open(output_filename, "a+")

# if the file is empty, write header
output_file.seek(0)

if output_file.read() == '':
    output_file.write("h, min, s, pm_25, pm_10\n")
    print("Created new output file")
else:
    print("Appending data to existing data file")

output_file.close()

print("h, min, sec, id, pm_25, pm_10")

while True:
    print("Waiting for data:")
    for ser in serials:
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

        output_file = open(output_filename, "a+")
        output_file.write(output_string)
        output_file.close()

        print(output_string)
    time.sleep(0.95)
