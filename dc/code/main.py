# main.py

# Replace this file with one from UserConfig.
# Here's an example for Air Quality using the sht40+bmp280:

# this is the sensor config file, and also the main file of the module!

from time import sleep
from utilities.mqtt_out import publish
from hardware.ICs.sht40bmp280 import sample


# sensing loop
while True:
    sleep(1)
    publish(sample())
