#!/usr/bin/python3

import rospy
from sds011_reader.msg import PMValues
import serial
import time

from datetime import date, datetime

try:
    serials = [serial.Serial('/dev/ttyUSB0'),
               serial.Serial('/dev/ttyUSB1')]
except serial.serialutil.SerialException as e:
    print(e)
    rospy.logerr("Are all sensors connected?")
    serials = [serial.Serial('/dev/ttyUSB0')]

output_filename = "pm_data/" + "multi_sensor" + "_" + str(date.today()) + ".csv"

node_name = "sds011_reader"

# Todo expose these as config params
id_front = 12684
id_back = 12685

if __name__ == '__main__':

    rospy.init_node(node_name)
    pub_pm_front = rospy.Publisher("pm_values_front", PMValues)
    pub_pm_back = rospy.Publisher("pm_values_back", PMValues)
    for ser in serials:
      print("Connected to port " + ser.port)

    print(output_filename)

    # Todo check if directory exists
    output_file = open(output_filename, "a+")

    # if the file is empty, write header
    output_file.seek(0)

    if output_file.read() == '':
        output_file.write("h, min, s, id, pm_25, pm_10\n")
        print("Created new output file")
    else:
        print("Appending data to existing data file")

    output_file.close()

    print("h, min, sec, id, pm_25, pm_10")

    while not rospy.is_shutdown():
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

            pm_message = PMValues()
            pm_message.header.stamp = rospy.Time.now()
            pm_message.pm_10 = pm_10
            pm_message.pm_25 = pm_25
            pm_message.sensor_id = sensor_id
            if sensor_id == id_front:
                pm_message.header.frame_id = "Front_PM_sensor"
                pub_pm_front.publish(pm_message)
            if sensor_id == id_back:
                pm_message.header.frame_id = "Back_PM_sensor"
                pub_pm_back.publish(pm_message)

            print(output_string)
        time.sleep(0.95)
