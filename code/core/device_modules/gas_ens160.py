import traceback
import logging
import time

logger = logging.getLogger(__name__)

class ENS160:

    # Power Modes (write to address 0x10)
    SLEEP_MODE    = 0x00 ## Deep Sleep (very low power).
    IDLE_MODE     = 0x01 ## Idle mode (low-power standby).
    STANDARD_MODE = 0x02 ## Gas Sensing Mode.


    def __init__(self, config: dict={}, variables: dict={}):
        # Load config
        if config is None: # Also accept None being passed to this function
            config = {}    # In this case, use a blank dict to avoid "NoneType has no attribute 'get()'" below
        self.i2c_address = config.get('i2c_address', 0x53)

        # Load variables
        if variables is None:
            variables = {}
        self.eCO2_variable = variables.get('eCO2_var', 'eCO2') # In case the user wants to rename these variables in the blackboard / sensing stack / pipeline
        self.TVOC_variable = variables.get('TVOC_var', 'TVOC')
        self.AQI_variable = variables.get('AQI_var', 'AQI')

        self.i2c = None # Interface created in initialise()


    def initialise(self, interface):
        """Expects I2C interface supporting read_register(device_addr, mem_addr, n_bytes) and write_register(device_addr, mem_addr, data as list of ints)"""
        self.i2c = interface

        # Check chip ID
        chip_id_bytes = self.i2c.read_register(self.i2c_address, 0x00, 2) # read chip ID as 2 bytes from 0x00. If a different device is connected, it may not acknowledge this register.
        chip_id = ((chip_id_bytes[1] << 8) | chip_id_bytes[0]) # convert to single int
        if chip_id != 0x160:
            raise ValueError(f"Starting ENS160 but chip ID mismatch. Read {chip_id}, expected 0x160 == 352")

        # Startup with assumed conditions
        self.set_PWR_mode(self.STANDARD_MODE)
        self.set_temp_and_hum(ambient_temp=25.00, relative_humidity=50.00)


    def sample(self):
        """Sample air quality readings from ENS160 sensor.

        Ignore warmup phase etc.

        :return dict Dictionary of eCO2 (ppm), TVOC (ppb) and AQI against variables set in config
        """

        try:
            # resend power mode every sample in case of sensor reset
            self.set_PWR_mode(self.STANDARD_MODE)

            # Read raw data from sensor
            raw_data = self.i2c.read_register(self.i2c_address, 0x21, 5)

            # Process readings
            AQI = raw_data[0] # The air quality index calculated on the basis of UBA. 1-5 (Corresponding to five levels of Excellent, Good, Moderate, Poor and Unhealthy respectively)
            TVOC = raw_data[2] << 8 | raw_data[1] # Total Volatile Organic Comounds concentration in ppb.
            eCO2 = raw_data[4] << 8 | raw_data[3] # CO2 equivalent concentration in ppm calculated according to the detected data of VOCs and hydrogen.

            return {
                self.AQI_variable: AQI,
                self.TVOC_variable: TVOC,
                self.eCO2_variable: eCO2,
                }

        except Exception as e:
            logger.error(traceback.format_exc())
            raise e


    def set_PWR_mode(self, mode):
        '''Configure power mode of ENS160

        :param int mode SLEEP_MODE=0, IDLE_MODE=1 or STANDARD_MODE=2
        '''
        self.i2c.write_register(self.i2c_address, 0x10, [mode]) # write one byte to 0x10
        time.sleep(0.02)


    def set_temp_and_hum(self, ambient_temp, relative_humidity):
        '''Write ambient temperature and relative humidity into ENS160 for calibration and compensation of the measured gas data.

        :param float ambient_temp Compensate the current ambient temperature, float type, unit: C
        :param float relative_humidity Compensate the current ambient humidity, float type, unit: %rH
        '''
        temp = int((ambient_temp + 273.15) * 64 + 0.5)
        rh = int(relative_humidity * 512 + 0.5)

        buf = [
            temp & 0xFF,
            (temp & 0xFF00) >> 8,
            rh & 0xFF,
            (rh & 0xFF00) >> 8,
            ]

        self.i2c.write_register(self.i2c_address, 0x13, buf) # Writes 4 bytes starting at 0x13.
