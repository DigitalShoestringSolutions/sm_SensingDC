import datetime
import time
import traceback
import logging

logger = logging.getLogger(__name__)


class SingleSample:
    def __init__(self, config):
        self.period = config["period"]
        self.sensing_stack = None

    def initialise(self, sensing_stacks):
        if len(sensing_stacks) == 1:
            self.sensing_stack = sensing_stacks[0]
        elif len(sensing_stacks) > 1:
            self.sensing_stack = sensing_stacks[0]
            logger.warning("Multiple sensing stacks provided - module expects 1 - using first")

    def loop(self):
        var_dict = self.sensing_stack.execute()
        return self.period, var_dict


class MultiSampleMerged:
    def __init__(self, config):
        self.period = config["period"]
        self.sensing_stacks = None

    def initialise(self, sensing_stacks):
        self.sensing_stacks = sensing_stacks

    def loop(self):
        var_dict = {}
        for stack in self.sensing_stacks:
            var_dict = {**var_dict, **stack.execute()}
        return self.period, var_dict


class MultiSampleIndividual:
    def __init__(self, config):
        self.period = config["period"]
        self.sensing_stacks = None
        self.counter = 0

    def initialise(self, sensing_stacks):
        self.sensing_stacks = sensing_stacks

    def loop(self):
        stack = self.sensing_stacks[self.counter]
        var_dict = stack.execute()

        self.counter = self.counter + 1
        if self.counter >= len(self.sensing_stacks):
            self.counter = 0

        delay = self.period if self.counter == 0 else 0
        return delay, var_dict
