import traceback
import logging
import datetime
import random
import time

logger = logging.getLogger(__name__)

# if you need to add imports that must be pip installed, do it like this:
# pip_requirements = {"smbus2": "0.4.3"}


class MaskToShiftHours:

    def __init__(self, config, variables):
        # TODO: extract config variables
        # for example
        self.shift_start_raw = config.get("shift_start_time", "09:00")
        self.shift_end_raw = config.get("shift_end_time", "17:00")
        self.off_value = config.get("off_value", 0)

        self.shift_start = datetime.datetime.strptime(
            self.shift_start_raw, "%H:%M"
        ).time()
        self.shift_end = datetime.datetime.strptime(self.shift_end_raw, "%H:%M").time()

        # TODO: get blackboard variable names
        # for example
        self.var = variables.get("masked_var")

    def calculate(self, blackboard):
        try:
            # Get input variable from blackboard
            value = blackboard[self.var]
            if value is not None:
                __dt = -1 * (
                    time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
                )
                tz = datetime.timezone(datetime.timedelta(seconds=__dt))
                if (
                    self.shift_start <= datetime.datetime.now(tz=tz).time()
                    and datetime.datetime.now(tz=tz).time() <= self.shift_end
                    and datetime.datetime.now(tz=tz).weekday() < 5
                ):  # if during shift hours and not weekend
                    # do nothing during shift hours
                    return blackboard
                else:
                    blackboard[self.var] = self.off_value
            else:
                logger.warning(
                    f"MaskToShiftHours: required variable '{self.var}' not found in blackboard"
                )
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e
        return blackboard


class PeriodicMask:
    def __init__(self, config, variables):
        self.active_period = config.get("active_period", 10)  # minutes
        self.active_period_variance = config.get("active_period_variance", 0)  # minutes
        self.idle_period = config.get("idle_period", 10)  # minutes
        self.idle_period_variance = config.get("idle_period_variance", 0)  # minutes

        self.idle_percentage = config.get("idle_percentage", 0)  # percentage

        self.is_active = False
        period = self.idle_period + random.uniform(
            -self.idle_period_variance, self.idle_period_variance
        )
        self.next_switch_time = datetime.datetime.now() + datetime.timedelta(
            minutes=period
        )
        logger.info(f"PeriodicMask: Starting in IDLE state for {period} minutes till {self.next_switch_time}")

        self.variables_list = variables["variables_list"]

    def calculate(self, blackboard):
        try:
            if datetime.datetime.now() >= self.next_switch_time:
                self.is_active = not self.is_active
                if self.is_active:
                    period = self.active_period + random.uniform(
                        -self.active_period_variance, self.active_period_variance
                    )
                else:
                    period = self.idle_period + random.uniform(
                        -self.idle_period_variance, self.idle_period_variance
                    )
                self.next_switch_time = datetime.datetime.now() + datetime.timedelta(
                    minutes=period
                )
                logger.info(
                    f"PeriodicMask: Switching to {'ACTIVE' if self.is_active else 'IDLE'} state for {period} minutes till {self.next_switch_time}"
                )

            if self.is_active:
                return blackboard
            else:
                for var in self.variables_list:
                    if var in blackboard:
                        blackboard[var] = blackboard[var] * (self.idle_percentage / 100)
                return blackboard
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e
