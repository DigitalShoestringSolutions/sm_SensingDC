# PulseCounter.py 

# standard imports
import time

# installed imports
from gpiozero import Button


class PulseCounter:

    def __init__(self, pin_num, debounce_time=0.01):

        self.total_count = 0
        self._old_count = 0
        self._old_time = time.time()

        pulse_button = Button(pin_num, bounce_time=debounce_time)
        pulse_button.when_pressed = self.on_pulse

    def on_pulse(self):
        # minimal activity here for fast callback
        self.total_count += 1

    def __call__(self, rounding=3):
        """Return a dict containing current position and velocity
        Rounding should be either None or an int of decimal places"""
        return {
            "total_count": self.total_count,
            "density": self.get_recent_pulse_density(rounding) 
            }

    def get_recent_pulse_density(self, rounding=None):
        """Returns the number of pulses since this function was last called divided by the time since this function was last called
        Rounding should be either None or an int of decimal places.
        """

        # read position and timestamp. Copy once so pulses while this function is executing are not lost.
        new_count = self.total_count
        new_time = time.time()

        # Calculate detla
        delta_count = new_count - self._old_count
        delta_time = new_time - self._old_time
        density = delta_count / delta_time
        
        # Save read position and timestamp for next time
        self._old_count = new_count
        self._old_time = new_time

        if rounding is None:
            return density
        else:
            return round(density, rounding)
