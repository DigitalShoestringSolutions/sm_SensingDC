import traceback
import logging
import random
import datetime

logger = logging.getLogger(__name__)

class MockDeviceConstant:

    def __init__(self, config, variables):
        self.value = config.get('value')

        self.variable = variables['variable']

    def initialise(self, interface):
        pass

    def sample(self):
        try:
            return {self.variable: self.value}
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e

class MockDeviceRandom:

    def __init__(self, config, variables):
        self.min = config.get('min',0)
        self.max = config.get('max')

        self.variable = variables['variable']

    def initialise(self, interface):
        pass

    def sample(self):
        try:
            return {self.variable: random.uniform(self.min, self.max)}
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e


class MockDeviceRandomInt:

    def __init__(self, config, variables):
        self.min = config.get("min", 0)
        self.max = config.get("max")

        self.variable = variables["variable"]

    def initialise(self, interface):
        pass

    def sample(self):
        try:
            return {self.variable: random.randint(self.min, self.max)}
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e


# Not yet tested - used calculation/gen_simulation.py/PeriodicMask as alternative
class MockPeriodicDevice:
    def __init__(self, config, variables):
        self.active_min = config.get("active_min", 0)
        self.active_max = config.get("active_max")
        
        self.idle_min = config.get("idle_min", 0)
        self.idle_max = config.get("idle_max")
        
        self.active_period = config.get("active_period", 10)  # minutes
        self.active_period_variance = config.get("active_period_variance", 0)  # minutes
        self.idle_period = config.get("idle_period", 10)      # minutes
        self.idle_period_variance = config.get("idle_period_variance", 0)  # minutes
        
        self.is_active = False
        self.next_switch_time = datetime.datetime.now() + datetime.timedelta(
            minutes=self.idle_period + random.uniform(-self.idle_period_variance, self.idle_period_variance)
        )

        self.variable = variables["variable"]

    def initialise(self, interface):
        pass

    def sample(self):
        try:
            if datetime.datetime.now() >= self.next_switch_time:
                self.is_active = not self.is_active
                if self.is_active:
                    period = self.active_period + random.uniform(-self.active_period_variance, self.active_period_variance)
                else:
                    period = self.idle_period + random.uniform(-self.idle_period_variance, self.idle_period_variance)
                self.next_switch_time = datetime.datetime.now() + datetime.timedelta(minutes=period)
            
            
            if self.is_active:
                return {self.variable: random.uniform(self.active_min, self.active_max)}
            else:
                return {self.variable: random.uniform(self.idle_min, self.idle_max)}
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e
