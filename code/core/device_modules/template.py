import traceback
import logging

logger = logging.getLogger(__name__)

# if you need to add imports that must be pip installed, do it like this:
# pip_requirements = {"smbus2": "0.4.3"}

class DeviceClassName:
    ADCMax = pow(2, 12)

    def __init__(self, config, variables):
        # TODO: extract config variables
        # for example
        self.variable_name = config.get("name_of_config_var_in_config","default_value")
        
        
        # TODO: prepare interface
        # for example
        self.i2c = None
        
        # TODO: get blackboard variable names
        # for example
        self.adc_voltage = variables["v_adc"]

    def initialise(self, interface):
        # TODO: save interface
        # (the received interface is defined in the config file, in this example we assume I2C)
        self.i2c = interface

    def sample(self):
        try:
            # TODO: sample the device
            address = 0x80
            num_bytes = 2
            readings = self.i2c.read_register(self.i2c_address,address, num_bytes) 
            
            result = (readings[1] << 8) + readings[0]

            return {self.adc_voltage: result}   # return dict of values to be added to blackboard
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e
