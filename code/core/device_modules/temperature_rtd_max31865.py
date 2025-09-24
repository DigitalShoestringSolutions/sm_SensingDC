import traceback
import logging
import time

logger = logging.getLogger(__name__)

class MAX31865:

    # Registers
    REG_CONFIG_READ = 0x00
    REG_CONFIG_WRITE = 0x80
    REG_RTD_READING = 0x01


    def __init__(self, config, variables):
        # Load config
        if config is None:                                   # Also accept None being passed to this function
            config = {}                                      # In this case, use a blank dict to avoid "NoneType has no attribute 'get()'" below
        self.R_Ref = config.get("R_Ref", 430)	             # ADC full scale. Ideally around 4*R_0dC. Product we recommend is specified to have a 430Ω 0.1% resistor.
        self.filter = config.get("filter_frequency", "50Hz") # What digital filter to apply to the data. 50Hz or 60Hz acceptable.
        self.continous = config.get("continuous", 1)         # Whether to sample continuously (1) (recommended), or wait until externally requested before taking a reading (0).
        assert self.continous in [0, 1]

        # Load variables
        if variables is None:
            variables = {}
        self.input_variable = variables.get('PT_RTD_resistance', 'resistance') # Physical input to the sensing hardware that this is modeling

        self.spi = None                                      # Interface created in initialise()
        self.spi_mode = 0b11                                 # MAX31865 only works with SPI clock polarity=1 and clock phase=1. Force during transfers.


    def initialise(self, interface):
        self.spi = interface

        self.set_config_reg(
            VBias=1, # even in discontinuous mode, keep VBias on.
            continuous=self.continous,
            filter50Hz=1 if self.filter=="50Hz" else 0
            )


    def sample(self) -> dict:
        try:
            if not self.continous:
                self.oneshot()
                time.sleep(0.1) # after activating oneshot measurement, conversion takes about 60ms until DATA_READY falls low (=ready). 100ms is safe margin.

            reading_bytes = self._read_regs(self.REG_RTD_READING, 2)
            adc_code = ((reading_bytes[0] << 8 | reading_bytes[1]) >> 1) # 15 bit data, discard fault bit
            resistance = self.R_Ref * adc_code / 32768 # Notably not 32767, see datasheet.

            return {self.input_variable: resistance}
    
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e


    def _read_regs(self, first_reg_addr,  nregs=8):
        """Read nregs consecutive registers, starting from first_reg_addr

        Registers of the MAX31865:
        00h = Config
        01h = RTD MSBs
        02h = RTD LSBs
        03h = High Fault Threshold MSB
        04h = High Fault Threshold LSB
        05h = Low Fault Threshold MSB
        06h = Low Fault Threshold LSB
        07h = Fault Status
        """

        resp = self.spi.transfer([first_reg_addr] + [0]*nregs, mode=self.spi_mode)[1:] # Ignore first byte as it was while the command was being clocked in. Force mode 3.
        return resp

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
        
        self.spi.transfer([self.REG_CONFIG_WRITE, new_config_byte], mode=self.spi_mode) # force mode 3


    def oneshot(self):
        """Request a single reading without otherwise changing the config."""
        current_config = self._read_regs(self.REG_CONFIG_READ, 1)[0]
        new_config = (current_config  | 0b00100000)
        self.transfer([self.REG_CONFIG_WRITE, new_config], mode=self.spi_mode) # force mode 3
