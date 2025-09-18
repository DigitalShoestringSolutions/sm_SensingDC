import traceback
import logging

logger = logging.getLogger(__name__)


class MLX90614:

    def __init__(self, config, variables):
        self.i2c_address = config.get('i2c_address',0x5a)
        self.i2c = None # Interface created in initialise()

        self.input_variable = variables.get('object_temperature', "temperature") # Physical input to the sensing hardware that this is modeling

    def initialise(self, interface):
        self.i2c = interface
        # "The maximum frequency of the MLX90614 SMBus is 100 kHz" datasheet page 21. Does the shoestring i2c interface module support configuring the speed?

    def sample(self) -> dict:
        try:
            # perform reading
            raw_temp_reading = self.i2c.read_register(self.i2c_address, 0x07, 2, stop=False) # read 2 bytes starting at 0x07 (object temperature zone 1)

            # unpack bytes into single temperature float
            raw_temp_int = raw_temp_reading[1] << 8 | raw_temp_reading[0]
            temperature  = (raw_temp_int * 0.02) - 273.15 # report in degrees C

            return {self.input_variable: round(temperature, 2)} # temperature will always be a multiple of 0.01. Don't let any floating point issues change this.

        except Exception as e:
            logger.error(traceback.format_exc())
            raise e
