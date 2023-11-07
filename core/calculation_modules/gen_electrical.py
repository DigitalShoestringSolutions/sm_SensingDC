import math
import traceback
import logging

logger = logging.getLogger(__name__)

class RMSToPeak:
    one_over_sqrt_2 = 1 / math.sqrt(2)

    def __init__(self, config,variables):
        self.var_in = variables.get('var_in')
        self.var_out = variables.get('var_out')

    def calculate(self, var_dict):
        try:
            # Get variable containing output value
            value = var_dict[self.var_out]
            if value is not None:
                # Divide by sqrt 2 to get RMS
                value = value * self.one_over_sqrt_2
                # Set the input variable
                var_dict[self.var_in] = value
            else:
                logger.warning(f"RMSToPeak: output variable '{self.var_out}' not found")
        except Exception:
            logger.error(traceback.format_exc())
        return var_dict

class PowerToCurrent:
    def __init__(self, config,variables):
        self.line_voltage = config.get('line_voltage',230)
        self.phases = config.get('phases',1)

        self.power_in = variables.get('power_in')
        self.rms_current_out = variables.get('rms_current_out')

    def calculate(self, var_dict):
        try:
            # Get variable containing output value
            rms_current = var_dict[self.rms_current_out]
            if rms_current is not None:
                # Divide by sqrt 2 to get RMS
                power = self.phases * rms_current * self.line_voltage
                # Set the input variable
                var_dict[self.power_in] = power
            else:
                logger.warning(f"PowerToCurrent: output current variable '{self.rms_current_out}' not found")
        except Exception:
            logger.error(traceback.format_exc())
        return var_dict