import traceback
import logging

logger = logging.getLogger(__name__)

class DefaultConstants:
    def __init__(self, config,variables):
        self.value = config.get('value')
        self.variable = variables.get('variable')

    def calculate(self, var_dict):
        try:
            var_dict.setdefault(self.variable, self.value)
        except:
            pass
        return var_dict

class FixedConstants:
    def __init__(self, config,variables):
        self.value = config.get('value')
        self.variable = variables.get('variable')

    def calculate(self, var_dict):
        try:
            var_dict[self.variable] = self.value
        except:
            pass
        return var_dict