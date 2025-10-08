from smbus2 import SMBus
from smbus2 import i2c_msg as Msg
import logging
import time

logger = logging.getLogger(__name__)


pip_requirements = {"smbus2":"0.4.3"}

class I2C:
    def __init__(self,config):
        self.bus = config.get('bus', 1)
        self.i2c = SMBus()


    def initialise(self):
        self.i2c.open(self.bus)


    def read_register(self, device_address, register, num_bytes, stop=False, delay:float=None) -> list:
        """Read a number of registers from attached I2C device.

        :param int address:   I2C slave device address.
        :param register:      Memory register to read first data byte from. Single int <= 255 or list of ints each <= 255.
        :param int num_bytes: Number of sequential bytes to read.
        :paran bool stop:     (optional) If false, complete the reg write and data read in a single transaction.
        :param float delay:   (optional) Seconds to sleep for between writing register and reading back data.
        """
        if isinstance(register, int): # accept single-byte addresses as int, or multi-byte addresses as list only
            register = [register]
        write_reg_addr = Msg.write(device_address, register)
        read_reg_data = Msg.read(device_address, num_bytes)

        if stop or (delay is not None): # allow supplying delay as a kwarg while not supplying stop
            self.i2c.i2c_rdwr(write_reg_addr)
            if delay:
                time.sleep(delay)
            self.i2c.i2c_rdwr(read_reg_data)
        else:
            self.i2c.i2c_rdwr(write_reg_addr, read_reg_data)

        return list(read_reg_data)


    def read(self, device_address:int, num_bytes:int) -> list:
        """Read bytes from a device on the I2C bus without specifying a memory register

        :param int device_address: I2C slave device address.
        :param int num_bytes: Number of bytes to read from device
        """
        read_reg_data = Msg.read(device_address, num_bytes)
        self.i2c.i2c_rdwr(read_reg_data)
        return list(read_reg_data)


    def write(self, device_address:int, data):
        """Write bytes to a device on the I2C bus without specifying a memory register

        :param int device_address: I2C slave device address.
        :param data: Single int <= 255 or list of ints each <= 255 to write to device.
        """
        if isinstance(data, int): # accept single-byte data as int, or multi-byte data as list only
            data = [data]
        write_data = Msg.write(device_address, data)
        self.i2c.i2c_rdwr(write_data)


    def write_register(self, device_address:int, register:int, data):
        """Set memory address `register` on an I2C slave device to `data`.

        :param int device_address: I2C slave device address.
        :param register: Memory register to write to. Single int <= 255 or list of ints each <= 255.
        :param data: Single int <= 255 or list of ints each <= 255 to write to device memory.
        """
        if isinstance(register, int): # accept single-byte addresses as int, or multi-byte addresses as list only
            register = [register]
        if isinstance(data, int): # accept single-byte data as int, or multi-byte data as list only
            data = [data]
        self.write(device_address, [*register, *data])
