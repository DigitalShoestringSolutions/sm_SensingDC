import time
import traceback
import logging
from crc import Calculator, Configuration

logger = logging.getLogger(__name__)


pip_requirements = {"crc":"7.1.0"}

class SHT40:
    # constants
    SHT40_TRH_HIGH_REGISTER = 0xFD
    SHT40_TRH_MED_REGISTER = 0xF6
    SHT40_TRH_LOW_REGISTER = 0xE0
    
    SAMPLE_MODE_REGISTERS = {
        "high":SHT40_TRH_HIGH_REGISTER,
        "med":SHT40_TRH_MED_REGISTER,
        "low":SHT40_TRH_LOW_REGISTER
    }
    
    crc_calculator = Calculator(Configuration(
        width=8,
        polynomial=0x31,
        init_value=0xFF,
        final_xor_value=0x00,
        reverse_input=False,
        reverse_output=False,
    )
    )

    def __init__(self, config, variables):
        self.i2c_address = config.get("i2c_address", 0x44)
        
        resolution = config.get("resolution", "high")
        self.mode_register = self.SAMPLE_MODE_REGISTERS.get(resolution, None)
        if self.mode_register is None:
            logger.warning('Invalid resolution set in config, using default of "high"')
            self.mode_register = self.SAMPLE_MODE_REGISTERS.get(2)
            
        self.humidity_variable = variables["RH"]
        self.temperature_variable = variables["T"]


    def initialise(self, interface):
        self.i2c = interface

    def sample(self):
        try:
            # Read temperature and humidity bytes
            buffer_out = self.i2c.read_register(
                self.i2c_address, self.mode_register, 6, stop=True, delay=0.01
            )
            
            # extract temperature and humidity values
            raw_temperature = (buffer_out[0] << 8) + buffer_out[1]
            if not self.crc_calculator.verify(bytes(buffer_out[0:2]), buffer_out[2]):
                logger.warning("CRC Checksum on Temperature failed")
            
            raw_humidity = (buffer_out[3] << 8) + buffer_out[4]
            if not self.crc_calculator.verify(bytes(buffer_out[3:5]), buffer_out[5]):
                logger.warning("CRC Checksum on Humidity failed")
                
            temperature = self._calculate_temperature(raw_temperature)
            humidity = self._calculate_relativehumidity(raw_humidity)

            logger.debug(f"temperature: {temperature}")
            logger.debug(f"humidity: {humidity}")

            return {
                self.humidity_variable: humidity,
                self.temperature_variable: temperature,
            }
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e

    def _calculate_temperature(self, S_T):
        """Calculate a temperature from adc int"""
        T_degC = -45 + (175*S_T/65535)
        return T_degC

    def _calculate_relativehumidity(self, S_RH):
        """Calculate a relative humidity from adc int"""
        RH = -6 + (125*S_RH/65535)
        return RH
