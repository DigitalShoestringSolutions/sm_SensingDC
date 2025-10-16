import time
import traceback
import logging

logger = logging.getLogger(__name__)


class BMP280:
    """
    Using the following settings as defaults as recommended on page 19 of the data sheet for
    "handheld device low-power":

    | Mode   | Over-sampling setting | osrs_p | osrs_t | IIR filter coeff. | Timing             | ODR [Hz] | BW [Hz] |
    | Normal | Ultra high resolution | ×16    | ×2     | 4                 | tstandby = 62.5 ms | 10.0     | 0.92    |
    """

    # constants
    BMP280_CONFIG_REGISTER = 0xF5
    BMP280_CNTL_MEAS_REGISTER = 0xF4
    BMP280_STATUS_REGISTER = 0xF3

    BMP280_RESET_REGISTER = 0xE0
    BMP280_RESET_VALUE = 0xB6

    BMP280_CALIBRATION_REGISTER = 0x88
    BMP280_RESULT_REGISTER = 0xF7

    BMP280_OSRS_P_VALUES = {
        0: 0b000,
        1: 0b001,
        2: 0b010,
        4: 0b011,
        8: 0b100,
        16: 0b101,
    }

    BMP280_OSRS_T_VALUES = {
        0: 0b000,
        1: 0b001,
        2: 0b010,
        4: 0b011,
        8: 0b100,
        16: 0b101,
    }

    BMP280_FILTER_VALUES = {0: 0b000, 2: 0b001, 4: 0b010, 8: 0b011, 16: 0b100}

    BMP280_T_SB_VALUES = {
        "0.5ms": 0b000,  # binary mask
        "62.5ms": 0b001,
        "125ms": 0b010,
        "250ms": 0b011,
        "500ms": 0b100,
        "1000ms": 0b101,
        "2000ms": 0b110,
        "4000ms": 0b111,
    }

    def __init__(self, config, variables):
        self.i2c_address = config.get("i2c_address", 0x76)
        # self.differential = config.get("differential", False)

        self.mode = 0b11

        osrs_p_string = config.get("osrs_p", 16)
        self.osrs_p = self.BMP280_OSRS_P_VALUES.get(osrs_p_string, None)
        if self.osrs_p is None:
            logger.warning("Invalid osrs_p set in config, using default of 16")
            self.osrs_p = self.BMP280_OSRS_P_VALUES.get(16)

        osrs_t_string = config.get("osrs_t", 2)
        self.osrs_t = self.BMP280_OSRS_T_VALUES.get(osrs_t_string, None)
        if self.osrs_t is None:
            logger.warning("Invalid osrs_t set in config, using default of 2")
            self.osrs_t = self.BMP280_OSRS_T_VALUES.get(2)

        t_sb_string = config.get("t_sb", "62.5ms")
        self.t_sb = self.BMP280_T_SB_VALUES.get(t_sb_string, None)
        if self.t_sb is None:
            logger.warning("Invalid t_sb set in config, using default of 62.5ms")
            self.t_sb = self.BMP280_T_SB_VALUES.get("62.5ms")

        filter_string = config.get("filter", 4)
        self.filter = self.BMP280_FILTER_VALUES.get(filter_string, None)
        if self.filter is None:
            logger.warning("Invalid filter set in config, using default of 4")
            self.filter = self.BMP280_FILTER_VALUES.get(4)

        self.i2c = None

        self.pressure_variable = variables["P"]
        self.temperature_variable = variables["T"]

    def initialise(self, interface):
        self.i2c = interface
        self._initialise_bmp280()
        
        
    def _initialise_bmp280(self):
        # Fetch callibration data
        buffer_out = self.i2c.read_register(
            self.i2c_address, self.BMP280_CALIBRATION_REGISTER, 24
        )
        endian = "little"
        self.cal_dig_T1 = int.from_bytes(buffer_out[0:2], byteorder=endian, signed=False)
        self.cal_dig_T2 = int.from_bytes(buffer_out[2:4], byteorder=endian, signed=True)
        self.cal_dig_T3 = int.from_bytes(buffer_out[4:6], byteorder=endian, signed=True)

        self.cal_dig_P1 = int.from_bytes(buffer_out[6:8], byteorder=endian, signed=False)
        self.cal_dig_P2 = int.from_bytes(buffer_out[8:10], byteorder=endian, signed=True)
        self.cal_dig_P3 = int.from_bytes(buffer_out[10:12], byteorder=endian, signed=True)
        self.cal_dig_P4 = int.from_bytes(buffer_out[12:14], byteorder=endian, signed=True)
        self.cal_dig_P5 = int.from_bytes(buffer_out[14:16], byteorder=endian, signed=True)
        self.cal_dig_P6 = int.from_bytes(buffer_out[16:18], byteorder=endian, signed=True)
        self.cal_dig_P7 = int.from_bytes(buffer_out[18:20], byteorder=endian, signed=True)
        self.cal_dig_P8 = int.from_bytes(buffer_out[20:22], byteorder=endian, signed=True)
        self.cal_dig_P9 = int.from_bytes(buffer_out[22:24], byteorder=endian, signed=True)

        # set t_sb and filter using config byte
        config = self.make_config_byte()
        buffer_out = self.i2c.write_register(
            self.i2c_address, self.BMP280_CONFIG_REGISTER, [config]
        )

        # set p & t over sample and mode using control byte
        control = self.make_control_byte()
        buffer_out = self.i2c.write_register(
            self.i2c_address, self.BMP280_CNTL_MEAS_REGISTER, [control]
        )
        
        time.sleep(0.1) # give time to fill filter registers
        
    def _do_read(self):
        # Read 3 temperature bytes and 3 pressure bytes
        buffer_out = self.i2c.read_register(
            self.i2c_address, self.BMP280_RESULT_REGISTER, 6
        )
        # extract temperature and pressure values
        raw_pressure = (
            (buffer_out[0] << 16) + (buffer_out[1] << 8) + buffer_out[2]
        ) >> 4
        raw_temperature = (
            (buffer_out[3] << 16) + (buffer_out[4] << 8) + buffer_out[5]
        ) >> 4
        
        return raw_pressure, raw_temperature

    def sample(self):
        try:
            raw_pressure, raw_temperature = self._do_read()

            logger.debug(f"raw_pressure: {raw_pressure}")
            logger.debug(f"raw_temperature: {raw_temperature}")
            # check for bad values
            if raw_pressure == 0x80000 or raw_temperature == 0x80000:
                # device may not be initialised or something went wrong
                logger.warning("Invalid reading - performing soft reset on BMP280")
                # soft reset
                self.i2c.write_register(
                    self.i2c_address,self.BMP280_RESET_REGISTER,[self.BMP280_RESET_VALUE]
                )
                # startup time listed as 2 ms, wait 5 to be safe
                time.sleep(0.005)
                #reinitialise
                self._initialise_bmp280()
                # read again
                raw_pressure, raw_temperature = self._do_read()
                # if values are bad again, just continue, don't block here indefinitely - will either be better on the next sample or reset again

            # calibrate
            temperature = self.compensate_temperature(raw_temperature)
            pressure = self.compensate_pressure(raw_pressure)

            logger.debug(f"temperature: {temperature}")
            logger.debug(f"pressure: {pressure}")

            return {
                self.pressure_variable: pressure,
                self.temperature_variable: temperature,
            }
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e

    def make_config_byte(self):
        byte = 0x00

        byte |= (self.filter & 0b111) << 2
        byte |= (self.t_sb & 0b111) << 5

        return byte

    def make_control_byte(self):
        byte = 0x00

        byte |= self.mode & 0b11
        byte |= (self.osrs_p & 0b111) << 2
        byte |= (self.osrs_t & 0b111) << 5

        return byte

    # adapted from Appendix 1 of bmp280 data sheet
    def compensate_temperature(self, adc_T):
        var1 = ((adc_T / 16384.0) - (self.cal_dig_T1 / 1024.0)) * self.cal_dig_T2
        var2 = (
            ((adc_T / 131072.0) - (self.cal_dig_T1 / 8192.0))
            * ((adc_T / 131072.0) - (self.cal_dig_T1 / 8192.0))
        ) * self.cal_dig_T3
        self.t_fine = var1 + var2
        T = (var1 + var2) / 5120.0
        return T

    # adapted from Appendix 1 of bmp280 data sheet
    def compensate_pressure(self, adc_P):
        var1 = (self.t_fine / 2.0) - 64000.0
        var2 = var1 * var1 * self.cal_dig_P6 / 32768.0
        var2 = var2 + (var1 * self.cal_dig_P5 * 2.0)
        var2 = (var2 / 4.0) + (self.cal_dig_P4 * 65536.0)
        var1 = (
            (self.cal_dig_P3 * var1 * var1 / 524288.0) + (self.cal_dig_P2 * var1)
        ) / 524288.0
        var1 = (1.0 + (var1 / 32768.0)) * self.cal_dig_P1
        if var1 == 0.0:
            return 0  # avoid exception caused by division by zero

        p = 1048576.0 - adc_P
        p = (p - (var2 / 4096.0)) * 6250.0 / var1
        var1 = self.cal_dig_P9 * p * p / 2147483648.0
        var2 = p * self.cal_dig_P8 / 32768.0
        p = p + (var1 + var2 + self.cal_dig_P7) / 16.0
        return p
