import traceback
import logging
import time

logger = logging.getLogger(__name__)

class MAX31865:

    # Registers
    REG_CONFIG_READ = 0x00
    REG_CONFIG_WRITE = 0x80
    REG_RTD_READING = 0x01


    def __init__(self, config:dict={}, variables:dict={}):
        """Device module for using the MAX31865 RTD amplifier to measure resistance of an attached PT-RTD.
        
        :param dict config:    (otpional) Configure the device. `R_Ref`, `filter_frequency` and `continuous` can be provided as keys.
        :param dict variables: (optional) Set the variable names to push to the blackboard.  Currently the only key searched for is `PT_RTD_resistance`, default value is `resistance`.
        """
        # Load config
        self.R_Ref = config.get("R_Ref", 430)	             # ADC full scale. Ideally around 4*R_0dC. Product we recommend is specified to have a 430Ω 0.1% resistor.
        self.filter = config.get("filter_frequency", "50Hz") # What digital filter to apply to the data. 50Hz or 60Hz acceptable.
        self.continous = config.get("continuous", 1)         # Whether to sample continuously (1) (recommended), or wait until externally requested before taking a reading (0).
        assert self.continous in [0, 1]

        # Load variables
        self.input_variable = variables.get('PT_RTD_resistance', 'resistance') # Physical input to the sensing hardware that this is modeling

        # Interface placeholder and interface settings
        self.spi = None                                      # Interface created in initialise()
        self.spi_mode = 0b11                                 # MAX31865 only works with SPI clock polarity=1 and clock phase=1. Force during transfers.


    def initialise(self, interface):
        """Associate the interface with the sensor. Expects an SPI instance the supports `read()` and `write()`."""
        self.spi = interface

        self.set_config_reg(
            VBias=1, # even in discontinuous mode, keep VBias on.
            continuous=self.continous,
            filter50Hz=1 if self.filter=="50Hz" else 0
            )


    def sample(self) -> dict:
        """Sample the resistance of the attached RTD. 
        
        :return dict A dictionary containing the resistance of the RTD in Ohms. The key can be changed with the config dict when constructing this class.
        """
        try:
            if not self.continous:
                self.oneshot()
                time.sleep(0.1) # after activating oneshot measurement, conversion takes about 60ms until DATA_READY falls low (=ready). 100ms is safe margin.

            reading_bytes = self.spi.read(self.REG_RTD_READING, 2, mode=self.spi_mode) # Read 2 bytes from 0x01.
            adc_code = ((reading_bytes[0] << 8 | reading_bytes[1]) >> 1) # 15 bit data, discard fault bit
            resistance = self.R_Ref * adc_code / 32768 # Notably not 32767, see datasheet.

            return {self.input_variable: resistance}
    
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e


    def set_config_reg(self,
                   VBias=0,
                   continuous=0,
                   oneshot=0,
                   threewire=0,
                   faultdetect=0,
                   faultclear=0,
                   filter50Hz=0
                   ):
        """
        Overwrite the config register:
        ---------------
        :param int VBias:       Vbias (1=ON, 0=OFF). Needs to be on in either mode to get new readings.
        :param int continuous:  Conversion Mode (1=Auto/Continuous, 0=OFF/Manual)
        :param int oneshot:     1-shot (1=1-shot on, auto cleared)
        :param int threewire:   3-wire select (1=3 wire config, 0=2 or 4 wire config)
        :param int faultdetect: fault detection cycle (0=none, otherwise see data sheet)
        :param int faultclear:  fault status clear (1=Clear any fault, auto cleared)
        :param int filter50Hz:  50/60 Hz filter select (1=50Hz, 0=60Hz)
        """

        new_config_byte = (VBias << 7 | 
                           continuous << 6 | 
                           oneshot << 5 | 
                           threewire << 4 | 
                           faultdetect << 2 | 
                           faultclear << 1 | 
                           filter50Hz
                           )
        
        self.spi.write(self.REG_CONFIG_WRITE, new_config_byte, mode=self.spi_mode)


    def oneshot(self):
        """Request a single reading without otherwise changing the config."""
        current_config = self.spi.read(self.REG_CONFIG_READ, 1, mode=self.spi_mode)[0]
        new_config = (current_config  | 0b00100000)
        self.spi.write(self.REG_CONFIG_WRITE, new_config, mode=self.spi_mode)
