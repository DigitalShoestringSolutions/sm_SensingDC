import traceback
import logging

logger = logging.getLogger(__name__)


class DS18B20:

    ONEWIRE_ID_PREFIX = "28"  # 0x28 prefix on id for all DS18B20 sensors.
    SENSOR_TYPE = "DS18B20"
    
    def __init__(self, config:dict={}, variables:dict={}):
        
        # Extract config
        self.channel = config.get('channel', 1)         # channel number can be 1 or above.
        self.sensor_id = config.get('sensor_id', None)  # Alternatively, set an ID string directly. Overwrites channel.

        # Extract variables
        self.temperature_variable = variables.get("temperature", "temperature")

        # Interface placeholder
        self.w1 = None

        # Validate config
        if self.sensor_id is not None:
            if not self.sensor_id.startswith(self.ONEWIRE_ID_PREFIX):  # If id set, it should start with the correct prefix.
                raise ValueError(f"{self.SENSOR_TYPE} sensor id set manually but id {self.sensor_id} does not start with the required prefix {self.ONEWIRE_ID_PREFIX}")

        self.channel = int(self.channel)  # attempt to cast to int, raise ValueError if fail.


    def initialise(self, interface):
        """Accept a OneWire interface and determine onewire ID"""
        # Save onewire interface
        self.w1 = interface

        # Find w1 ID value. If sensor_id was specified in config, use that. Else, use the channel number as an index for the list of suitable sensors detected.
        all_devices_on_bus = self.w1.get_devices_on_bus()
        if self.sensor_id is not None:
            if self.sensor_id in all_devices_on_bus:
                self.w1_id == self.sensor_id
                logger.debug(f"Accepted {self.SENSOR_TYPE} sensor_id {self.sensor_id} set in config")
            else:
                raise ValueError(f"{self.SENSOR_TYPE} sensor id set manually but id {self.sensor_id} was not found on OneWire Bus")

        else:
            # Find all suitable devices on bus
            suitable_sensors_on_bus = []
            for device in all_devices_on_bus:
                if device.startswith(self.ONEWIRE_ID_PREFIX):  # Suitable sensor prefix depends on exactly which sensor type is being used
                    suitable_sensors_on_bus.append(device)
            logger.debug(f"suitable {self.SENSOR_TYPE} devices on w1 bus: {suitable_sensors_on_bus}")

            # Select one of those according to channel config
            try:
                self.w1_id = suitable_sensors_on_bus[self.channel - 1]  # channel config starts at 1
                logger.debug(f"Sensor id {self.w1_id} found for {self.SENSOR_TYPE} channel {self.channel}")
            except IndexError as e:
                # Add helpful info to the error message
                e.add_note(f"{self.SENSOR_TYPE} channel {self.channel} requested, but only {len(suitable_sensors_on_bus)} {self.SENSOR_TYPE}s were found on the OneWire bus")
                raise         


    def get_temperature(self) -> float:
        """Read temperature in degrees C"""
        # Read from sensor
        file = self.w1.read_file(self.w1_id)
        
        # Check CRC
        if file[0].strip()[-3:] != "YES":
            raise ValueError(f"{self.SENSOR_TYPE} id {self.w1_id} CRC failure")
        logger.debug(f"{self.SENSOR_TYPE} id {self.w1_id} CRC passed")

        # Extract temperature value
        temperature_str = file[1].strip().rsplit('t=')[1]
        temperature_C = int(temperature_str) / 1000
        return temperature_C


    def sample(self) -> dict:
        """Return the current temperature in degrees C in a dict against the key set in config"""
        try:
            return {self.temperature_variable: self.get_temperature()}

        except Exception as e:
            logger.error(traceback.format_exc())
            raise e



# I do not have these other sensors on hand to test, but they should behave similarly
class DS18S20(DS18B20):
   ONEWIRE_ID_PREFIX = "10"
   SENSOR_TYPE = "DS18S20"

class DS1822(DS18B20):
   ONEWIRE_ID_PREFIX = "22"
   SENSOR_TYPE = "DS1822"

class DS1825(DS18B20):
   ONEWIRE_ID_PREFIX = "3B"
   SENSOR_TYPE = "DS1825"

class DS28EA00(DS18B20):
   ONEWIRE_ID_PREFIX = "42"
   SENSOR_TYPE = "DS28EA00"
