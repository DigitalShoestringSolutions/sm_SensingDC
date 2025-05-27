import traceback
import logging

logger = logging.getLogger(__name__)

# if you need to add imports that must be pip installed, do it like this:
# pip_requirements = {"smbus2": "0.4.3"}

class CalcClassName:

    def __init__(self, config, variables):
        # TODO: extract config variables
        # for example
        self.variable_name = config.get("name_of_config_var_in_config","default_value")

        # TODO: get blackboard variable names
        # for example
        self.var_in = variables.get("blackboard_var_in")

        self.var_out = variables.get("blackboard_var_out")

    def calculate(self, blackboard):
        try:
            # Get input variable from blackboard
            value = blackboard[self.var_in]
            if value is not None:
                # TODO do calculation
                calc_result = 1

                # Set the input variable
                blackboard[self.var_out] = calc_result
            else:
                logger.warning(
                    f"CalcClassName: required variable '{self.var_in}' not found in blackboard"
                )
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e
        return blackboard
