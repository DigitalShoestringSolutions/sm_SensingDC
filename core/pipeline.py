import traceback
import logging

logger = logging.getLogger(__name__)

class Pipeline:
    def __init__(self,spec):
        self.spec = reversed(spec)
        self.contents = []

    def initialise(self,calculation_modules):
        for entry in self.spec:
            self.contents.append(calculation_modules[entry])

    def execute(self,sample_dict):
        variables_dict = {**sample_dict}
        for calc_module in self.contents:
            try:
                output = calc_module.calculate(variables_dict)
                variables_dict = output
            except Exception:
                logger.error(traceback.format_exc())
        return variables_dict