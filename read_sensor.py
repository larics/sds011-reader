import serial, datetime, time
import os

from datetime import date, datetime

ser = serial.Serial('/dev/ttyUSB_SDS011_PM_sensor')

print("Connected to /dev/ttyUSB_SDS011_PM_sensor")

identity = os.environ['IDENTITY']
output_filename = "data/" + identity + "_" + str(date.today()) + ".csv"
print(output_filename)

output_file = open(output_filename, "a+");

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
    print("Waiting for data:");
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

    output_file = open(output_filename, "a+");
    output_file.write(output_string)
    output_file.close()

    print(output_string)
