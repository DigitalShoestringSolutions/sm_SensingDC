import spidev

pip_requirements = {"spidev":"3.6"}

class SPI:
    def __init__(self,config):
        self.bus = config.get('bus', 0)
        self.device = config.get('device', 0)
        self.default_speed = config.get('speed', 1000000)
        self.default_mode = config.get('mode', 0)
        self.spi = spidev.SpiDev()

    def initialise(self):
        self.spi.open(self.bus, self.device)

    def transfer(self, bytes,mode = None,speed = None):
        self.spi.mode = self.default_mode if mode is None else mode
        self.spi.max_speed_hz  = self.default_speed if speed is None else speed
        return self.spi.xfer2(bytes)

    def read(self, reg, n_words: int=1, mode: int=None, speed_hz: int=None) -> list:
        """Clocks `reg` into the SPI device, then clock out `n_words` more words. 
        
        Unless bits per word has been altered, words typically equate to bytes.

        :param reg:         The register to be clocked into the device before reading. Single int or list of ints.
        :param int n_words: (optional) The number of words to read. Default 1.
        :param int mode:    (optional) Change the bus config before the transaction. `(clock polarity << 1 | clock phase)` as a 2 bit int.
        :param int speed:   (optional) Change the bus config before the transaction. Set SPI clock speed in Hz.
        :return:            list of integers        
        """
        if isinstance(reg, int):
            reg = [reg]
        return self.transfer(reg + [0]*n_words, mode=mode, speed=speed_hz)[1:] # The first word returned is discarded, as it was while the reg was being clocked in.

    def write(self, reg, data, mode: int=None, speed_hz: int=None) -> None:
        """Write `reg` to the SPI device, then write `data` to the SPI device. Either can be an int for a single word/byte, or a list of ints for multiple words/bytes.

        :param reg:       The register to be clocked into the device before writing `data`. Single int or list of ints.
        :param data:      The words to be written after `reg`. Single int or list of ints.
        :param int mode:  (optional) Change the bus config before the transaction. `(clock polarity << 1 | clock phase)` as a 2 bit int.
        :param int speed: (optional) Change the bus config before the transaction. Set SPI clock speed in Hz.
        """
        if isinstance(reg, int):
            reg = [reg]
        if isinstance(data, int):
            data = [data]
        self.transfer(reg + data, mode=mode, speed=speed_hz)
