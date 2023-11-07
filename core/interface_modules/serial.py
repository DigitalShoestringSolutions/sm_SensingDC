import serial

class Serial:
    def __init__(self,config):
        self.port = config['port']
        self.baud = config['baud']
        self.serial = None

    def initialise(self):
        self.serial = serial.Serial(self.port,self.baud )

    def read(self):

        return {'data':12345}

    def write(self):
        pass