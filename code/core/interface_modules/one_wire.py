import os
import logging

logger = logging.getLogger(__name__)

class OneWire:

    def __init__(self, config={}):  # :param config not used but must be handled
        # supports GPIO4 only!
        # would be nice to support other pins, or be able to apply a software pull-up.
        self.devices_dir = "/sys/bus/w1/devices/"  # dtoverlay for pin4


    def initialise(self):
        if os.path.exists(self.devices_dir):
            logger.debug(f"One wire bus found at {self.devices_dir}")
        else:
            logger.error(f"One wire bus not found at {self.devices_dir}")


    def get_devices_on_bus(self) -> list:
        # Detect devices
        devices = os.listdir(self.devices_dir)

        # If w1_bus_master1 is in devices list, remove it
        try:
            devices.remove("w1_bus_master1")
        except ValueError:
            pass

        return devices


    def _get_filepath(self, id: str, validate: bool = True) -> str:
        """Get the full filepath of a device on the w1 bus

        :param str id:        w1 hex address, directory name
        :param bool validate: (optional) Test if the file exists before returning. Default True.
        """
        filepath = self.devices_dir + id + "/w1_slave"

        # Validate file exists
        if validate:
            try:
                with open(filepath, "r"):
                    pass
            except FileNotFoundError as e:
                e.add_note(f"Attempting to communicate with OneWire device {id} but file {filepath} not found")
                raise

        return filepath


    def read_file(self, id):
        filepath = self._get_filepath(id) 
        with open(filepath, 'r') as f:
            lines = f.readlines()

            try:
                line0 = lines[0] # Test if file is empty by seeing if first line exists
            except IndexError as e:
                e.add_note(f"OneWire device file {filepath} is empty, communication unsuccessful?")
                raise

            return lines

