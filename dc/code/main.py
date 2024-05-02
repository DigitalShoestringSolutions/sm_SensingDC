# main.py

# Replace this file with one from UserConfig.
# Here's an example for Air Quality using the sht40+bmp280:

# this is the sensor config file, and also the main file of the module!

# This build demonstrates effortless combination on sensors

from time import sleep
from utilities.mqtt_out import publish
from hardware.ICs.sht40 import SHT40
from hardware.ICs.bmp280_wrapper import BMP280

# setup sensors and models
mysht40 = SHT40()
mybmp280 = BMP280()

# sensing loop
while True:
    sleep(1)
    publish( mysht40.get_TRH() | mybmp280.get_P() )
