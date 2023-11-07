import traceback
import logging

logger = logging.getLogger(__name__)

class MockDevice:

    def __init__(self, config, variables):
        self.value = config.get('value')

        self.variable = variables['variable']

    def initialise(self, interface):
        pass

    def sample(self):
        try:
            return {self.variable: self.value}
        except Exception:
            logger.error(traceback.format_exc())
            return {}
