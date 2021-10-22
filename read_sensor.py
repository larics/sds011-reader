import serial, datetime, time

from datetime import date, datetime

ser = serial.Serial('/dev/ttyUSB_SDS011_PM_sensor')

print("Connected to /dev/ttyUSB_SDS011_PM_sensor")

output_file = open("data/" + str(date.today()) + ".csv", "a+");

# if the file is empty, write header
output_file.seek(0)
if output_file.read() == '':
    output_file.write("h, min, s, pm_25, pm_10\n")
    print("Created new output file")
else:
    print("Appending data to existing data file")

print("h, min, sec, pm_25, pm_10")

while True:
    print("Waiting for data:");
    data = []
    for index in range(0, 10):
        datum = ser.read()
        data.append(datum)

    pm_25 = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
    pm_10 = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10

    now = datetime.now()
    output_string = str(now.hour) + ', ' + str(now.minute) + ', ' \
      + str(now.second) + ', ' + str(pm_25) + ', ' + str(pm_10) + '\n'

    output_file.write(output_string)

    print(output_string)
