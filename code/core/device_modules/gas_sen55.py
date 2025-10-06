import traceback
import logging
import time

logger = logging.getLogger(__name__)

class SEN55:
    def __init__(self, config: dict={}, variables: dict={}):
        """Device Module for reading data from the SEN55 particulate matter air sensor.

        CRC is ignored when reading data from device.

        :param dict config:    (otpional) Configure the device. Currrently the only key searched for is `i2c_address` (defaults to 0x69).
        :param dict variables: (optional) Set the variable names to push to the blackboard. See source code for the 8 keys.
        """
        # Load config
        self.i2c_address = config.get('i2c_address', 0x69)

        # Load variables
        self.pm1_var  = variables.get('PM1_var'              , 'mc_1p0') # In case the user wants to rename these variables in the blackboard / sensing stack / pipeline
        self.pm25_var = variables.get('PM2.5_var'            , 'mc_2p5') # Default variable names match APM v1.x.x
        self.pm4_var  = variables.get('PM4_var'              , 'mc_4p0')
        self.pm10_var = variables.get('PM10_var'             , 'mc_10p0')
        self.voc_var  = variables.get('voc_var'              , 'voc_index')
        self.nox_var  = variables.get('nox_var'              , 'nox_index')
        self.t_var    = variables.get('temperature_var'      , 'ambient_t')
        self.rh_var   = variables.get('relative_humidity_var', 'ambient_rh')

        # Interface placeholder
        self.i2c = None # Interface created in initialise()


    def initialise(self, interface):
        """Expects I2C interface supporting read_register(device_addr, mem_addr, n_bytes) and write_register(device_addr, mem_addr, data as list of ints)"""
        self.i2c = interface

        # wait 1 s for sensor start up (> 1000 ms according to datasheet)
        time.sleep(1)

        # Check product name in device memory matches expectations
        name = self.get_product_name()
        if name[0:9] == [83, 69, 131, 78, 53, 85, 53, 0, 68]: # SEN55 in ASCII with checksum every 2 bytes.
            print("read product name SEN55 as expected")
        else:
            error_message = f"Starting SEN55 but chip ID mismatch. Device detected at {self.i2c_address} but read {name}, expected [83, 69, 131, 78, 53, 85, 53, 0, 68 ...]"
            logger.error(error_message)
            raise ValueError(error_message)

        logger.info("SEN55 serial number:", self.get_serial_number())
        logger.info("SEN55 firmware version:", self.get_firmware_version())

        # Set to full power mode
        self.start_measurement()

        # wait for first measurement to be finished
        time.sleep(2)


    def start_measurement(self):
        """Activate all parameter measurement mode."""
        self.i2c.write(self.i2c_address, 0x0021)
        time.sleep(0.05)


    def stop_measurement(self):
        """Return to idle mode."""
        self.i2c.write(self.i2c_address, 0x0104)
        time.sleep(0.2) # specified max execution time for stop command. Attempting next I2C transaction sooner may NAK -> Remote I/O error, or data will be 0xFF


    @property
    def data_ready(self):
        """Is the Data Ready flag currently set?"""
        buf = self.i2c.read_register(self.i2c_address, 0x0202, 3, stop=True, delay=0.02) # 1 empty byte + 1 containing flat + 1 CRC
        if buf == [0, 1, 176]:
            return True
        elif buf == [0, 0, 129]:
            return False
        else:
            raise ValueError("Unexpected value when polling SEN55 data ready. Possible CRC failure")


    def get_product_name(self):
        """SEN50, SEN54 or SEN55 in ASCII with checksum every 2 bytes."""
        product_name = self.i2c.read_register(self.i2c_address, 0xD014, 48, stop=True, delay=0.02)
        return product_name # with CRC bytes included


    def get_serial_number(self):
        serial_number = self.i2c.read_register(self.i2c_address, 0xD033, 48, stop=True, delay=0.02)
        return serial_number # with CRC bytes included


    def get_firmware_version(self):
        firmware_version = self.i2c.read_register(self.i2c_address, 0xD100, 3, stop=True, delay=0.02) # 1 byte f/w vn, 1 byte reserved and 1 CRC
        return firmware_version[0] # just firmware version integer. Expect 2.


    def sample(self):
        """Sample all air metrics from the SEN55 sensor.

        :return dict Dictionary of particulate matter, voc/nox, temperature and humidity against variables set in when creating class instance
        """

        try:
            if not self.data_ready:
                raise ValueError("SEN5x data is not ready")

            #self.i2c.write(self.i2c_address, 0x03C4) # Request data. Enter Read Measured Values command (0x03C4)
            #time.sleep(0.02) # Wait 20ms for data ready. "After 20 ms, the read data header can be sent..." datasheet page 19
            #raw_data = self.i2c.read(self.i2c_address, 24) # Read 24 bytes from device. Each three bytes in a sequence of MSB, LSB, CRC. Reading from this reg resets the Data-Ready Flag

            # Or do the above 3 steps all in one:
            raw_data = self.i2c.read_register(self.i2c_address, 0x03C4, 24, stop=True, delay=0.02)

            # Process raw data into floats
            pm1p0  = (raw_data[0] << 8 | raw_data[1])  / 10
            pm2p5  = (raw_data[3] << 8 | raw_data[4])  / 10
            pm4p0  = (raw_data[6] << 8 | raw_data[7])  / 10
            pm10p0 = (raw_data[9] << 8 | raw_data[10]) / 10

            humidity = (raw_data[12] << 8 | raw_data[13]) / 100

            temperature = (raw_data[15] << 8 | raw_data[16]) / 200

            voc = (raw_data[18] << 8 | raw_data[19]) / 10
            nox = (raw_data[21] << 8 | raw_data[22]) / 10

            # Return data as dict using keys set with `variables` at class instance creation
            return {
                self.pm1_var  : pm1p0,
                self.pm25_var : pm2p5,
                self.pm4_var  : pm4p0,
                self.pm10_var : pm10p0,
                self.voc_var  : voc,
                self.nox_var  : nox,
                self.t_var    : temperature,
                self.rh_var   : humidity
            }

        except Exception as e:
            logger.error(traceback.format_exc())
            raise e
