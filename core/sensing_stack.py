import traceback
import logging

logger = logging.getLogger(__name__)


class SensingStack:
    def __init__(self, config):
        self.device_tag = config['device']
        self.pipeline_tag = config['pipeline']
        self.prefix = config.get('prefix')
        self.constants = config.get('constants')

        self.device = None
        self.pipeline = None

    def initialise(self, devices, pipelines):
        self.device = devices[self.device_tag]
        self.pipeline = pipelines[self.pipeline_tag]

    def execute(self):
        sample_dict = self.device.sample()
        output_dict = self.pipeline.execute(sample_dict)
        if self.constants is not None:
            output_dict = {**self.constants, **output_dict}

        if self.prefix is not None:
            return {self.prefix + key: value for key, value in output_dict.items()}
        else:
            return output_dict
