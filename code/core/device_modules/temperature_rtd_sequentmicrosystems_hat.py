import traceback
import logging
import struct

logger = logging.getLogger(__name__)


class Sequent_8ch_RTD_HAT:

    def __init__(self, config:dict={}, variables:dict={}):
        """Device module for using the Sequent Microsystems RTD DAQ HAT to measure resistance of an attached PT-RTD.

        This hardware supports only PT-RTDs with a nominal resistance of 100 Ohms. Multiple RTDs can be connected to this HAT at once and selected with `channel`.

        :param dict config:    (otpional) Configure the device. Currrently the keys searched for are `channel` (1-8) and `i2c_address` (defaults to 0x40, increases with stack number).
        :param dict variables: (optional) Set the variable names to push to the blackboard.  Currently the only key searched for is `PT_RTD_resistance`, default value is `resistance`.
        """
        # Load config
        self.channel = config.get('channel')                 # No default value here, must be configured
        self.i2c_address = config.get('i2c_address', 0x40)   # Use stack number? In the case of this HAT, that is as simple as just 0x40 + stack

        # Load variables
        self.input_variable = variables.get('PT_RTD_resistance', 'resistance') # Physical input to the sensing hardware that this is modeling

        # Interface placeholder
        self.i2c = None                                      # Interface created in initialise()


    def initialise(self, interface):
        """Associate the interface with the sensor. Expects an I2C instance the supports `read_register()`"""
        self.i2c = interface


    def read_resistance(self, channel) -> float:
        """Sample the resistance of the attached RTD. 

        :param int channel: Multiple RTDs can be connected to this hardware. Select which to sample from. Uses the same numbering scheme as silkscreen, must be between 1 and 8 inclusive.
        :return float Resistance of the RTD in Ohms
        """
        # Check channel number is valid. Must be an int between 1 and 8 inclusive.
        if not isinstance(channel, int):
            raise TypeError(f"Sequent_8ch_RTD_HAT supplied with channel {channel} which is a {type(channel)} not an int")
        elif (channel < 1) or (channel > 8):  # As marked on silkscreen, this HAT's lowest channel is 1.
            raise ValueError(f"Sequent_8ch_RTD_HAT supplied with channel number {channel}, cannot be <1 or >8")

        # identify target register 
        register_addr =  59 + (4 * (channel - 1))

        # perform reading
        readings = self.i2c.read_register(self.i2c_address, register_addr, 4, stop=False) # read 4 bytes starting at register_addr

        # unpack bytes into single resistance float
        resistance = struct.unpack('f', bytearray(readings))[0]

        return resistance


    def sample(self) -> dict:
        """Sample the resistance of the attached RTD. 

        Channel cannot be selected here, that must be done with `config` when constructing the class.

        :return dict A dictionary containing the resistance of the RTD in Ohms. The key can be changed with the config dict when constructing this class.
        """
        try:
            resistance = self.read_resistance(self.channel)
            return {self.input_variable: resistance}

        except Exception as e:
            logger.error(traceback.format_exc())
            raise e
