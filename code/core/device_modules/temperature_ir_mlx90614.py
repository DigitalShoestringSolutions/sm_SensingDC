import traceback
import logging

logger = logging.getLogger(__name__)


class MLX90614:

    def __init__(self, config:dict={}, variables:dict={}):
        """Device module for using the MLX90614 IR temperature sensor to measure the temperature of an object by its infrared emissions.

        :param dict config:    (otpional) Configure the device. Currrently the only key searched for is `i2c_address` (defaults to 0x5a).
        :param dict variables: (optional) Set the variable names to push to the blackboard. Currently the only key searched for is `object_temperature`, default value is `temperature`.
        """
        # Load config
        self.i2c_address = config.get('i2c_address', 0x5a)

        # Load variables
        self.input_variable = variables.get('object_temperature', "temperature") # Physical input to the sensing hardware that this is modeling

        # Interface placeholder
        self.i2c = None # Interface created in initialise()


    def initialise(self, interface):
        """Associate the interface with the sensor. Expects an I2C instance the supports `read_register()`"""
        self.i2c = interface
        # "The maximum frequency of the MLX90614 SMBus is 100 kHz" datasheet page 21. Does the shoestring i2c interface module support configuring the speed?


    def read_temperature(self) -> float:
        """Read the IR temperature from the sensor in Kelvin."""
        # perform reading
        raw_temp_reading = self.i2c.read_register(self.i2c_address, 0x07, 2, stop=False) # read 2 bytes starting at 0x07 (object temperature zone 1)

        # unpack bytes into single temperature float
        raw_temp_int = raw_temp_reading[1] << 8 | raw_temp_reading[0] # raw_temp_int = kelvin*50
        temperature  = raw_temp_int * 0.02        
        temperature = round(temperature, 2) # temperature will always be a multiple of 0.02. Don't let any floating point issues change this.

        return temperature


    def sample(self) -> dict:
        """"Read the IR temperature from the sensor.

        Resolution is 0.02 C.

        :return dict A dictionary containing the sampled temperature in C. The key can be changed with the config dict when constructing this class.
        """
        try:
            temperature = self.read_temperature() - 273.15 # report in degrees C
            return {self.input_variable: temperature}

        except Exception as e:
            logger.error(traceback.format_exc())
            raise e
