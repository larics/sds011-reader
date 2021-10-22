# SDS011 PM sensor reader

Read data from the SDS011 PM sensor in active reporting mode.

## Setup

Use uart rules to create a persistent name for your device. Write the following line into a .rules file. For example `/etc/udev/rules.d/50-local.rules`

    SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", SYMLINK+="ttyUSB_SDS011_PM_sensor"

## Usage

Run the read\_sensor.py script with python3. It will create a `<today's_date>.csv` file and populate it with measurements.

    $ python3 read_sensor.py
