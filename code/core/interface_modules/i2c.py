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


    def read_register(self,address,register,num_bytes,stop=False, delay:float=None):     # Write address, register_no  -- Read address, data
        """Read a number of registers from attached I2C device.

        :param int address:   I2C slave device address.
        :param int register:  Memory register to read first data byte from.
        :param int num_bytes: Number of sequential bytes to read.
        :paran bool stop:     (optional) If false, complete the reg write and data read in a single transaction.
        :param float delay:   (optional) Seconds to sleep for between writing register and reading back data. Requires `stop=True` to be effective.
        """
        register = self._data_to_list(register) # accept multi-byte addresses
        write_reg_addr = Msg.write(address, register)
        read_reg_data = Msg.read(address,num_bytes)

        if stop:
            self.i2c.i2c_rdwr(write_reg_addr)
            if delay:
                time.sleep(delay)
            self.i2c.i2c_rdwr(read_reg_data)
        else:
            self.i2c.i2c_rdwr(write_reg_addr, read_reg_data)

        return list(read_reg_data)


    def read(self, device_address:int, num_bytes:int):
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
        :param data: int or list of ints (each max 255) to write to device.
        """
        data = self._data_to_list(data) # accept multi-byte data in single int
        msg = Msg.write(device_address, data)
        self.i2c.i2c_rdwr(msg)


    def write_register(self, device_address:int, register:int, data):
        """Set memory address `register` on an I2C slave device to `data`.

        :param int device_address: I2C slave device address.
        :param int register: Memory register to write to.
        :param data: Single int or list of ints (each max 255) to write to device memory.
        """
        register = self._data_to_list(register) # accept multi-byte addresses
        data = self._data_to_list(data) # accept multi-byte data in single int
        self.write(device_address, [*register, *data])


    def _data_to_list(self, data):
        """Turns an int into a list of ints < 255. If not an int, returns the input.

        192 -> [192]
        0xC0FFEE -> [192, 255, 238]
        [192, 168] -> [192, 168]
        """
        if isinstance(data, int):
            if data == 0:
                return [0] # handle edge case where below loop would return [] rather than desired [0]
            else:
                data_list = []
                while data > 0:
                    data_list.insert(0, data & 0xFF)
                    data = data >> 8
                return data_list
        else:
            return data # unchanged
