# main.py

# Replace this file with one from UserConfig.
# Here's an example for EncoderMonitoring:

# this is the sensor config file, and also the main file of the module!

from time import sleep
from utils.mqtt_out import publish
from hardware.generic.encoderwheel import EncoderWheel

# setup sensors and models
ConveyorEncoder = EncoderWheel(14, 15, 1024, circ=0.2)

# sensing loop
while True:
    sleep(1)
    report = "encoder position is " + str(ConveyorEncoder())
    publish(report)
