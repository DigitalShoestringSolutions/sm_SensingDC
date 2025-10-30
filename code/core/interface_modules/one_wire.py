import os
import logging

logger = logging.getLogger(__name__)

class OneWire:

    def __init__(self):  # supports GPIO4 only!
        # would be nice to support other pins, or be able to apply a software pull-up.
        self.devices_dir = "/sys/bus/w1/devices/" # dtoverlay for pin4

        if not os.path.exists(self.self.devices_dir):
            logger.error(f"One wire device not found at {self.self.devices_dir}")
        
    def get_devices_on_bus(self) -> list:
        # Detect devices
        devices = os.listdir(self.devices_dir)

        # If w1_bus_master1 is in devices list, remove it
        try:
            devices.remove("w1_bus_master1")
        except ValueError:
            pass

        return devices

    def _get_filepath(self, id:str) -> str:
        return self.devices_dir + id + "/w1_slave"

    def read_file(self, id):
        with open(self._get_filepath(id), 'r') as f:
            return f.readlines()

