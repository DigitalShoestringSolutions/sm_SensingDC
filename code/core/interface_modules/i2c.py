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

        # Express register as a list of ints < 255
        if register == 0:
            write_data = [register]
        else:
            write_data = []
            while register > 0:
                write_data.insert(0, register & 0xFF)
                register = register >> 8

        write_reg_addr = Msg.write(address, write_data)
        read_reg_data = Msg.read(address,num_bytes)

        if stop:
            self.i2c.i2c_rdwr(write_reg_addr)
            if delay:
                time.sleep(delay)
            self.i2c.i2c_rdwr(read_reg_data)
        else:
            self.i2c.i2c_rdwr(write_reg_addr, read_reg_data)

        return list(read_reg_data)

    def write_register(self,address,register,data):    #Write address, register, data...
        write_reg_addr_data = Msg.write(address,[register,*data])
        self.i2c.i2c_rdwr(write_reg_addr_data)
