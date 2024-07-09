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

        self.pulse_button = Button(pin_num, bounce_time=debounce_time)
        self.pulse_button.when_pressed = self.on_pulse

    def on_pulse(self):
        # minimal activity here for fast callback
        self.total_count += 1

    def __call__(self, rounding: int = 3) -> dict:
        """Return a dict containing the count of recently occurred pulses and their time density.
        Rounding should be either None or an int of decimal places
        """
        count, density = self.recent_pulses_and_density(rounding)
        return {
            "count": count,
            "density": density
            }

    def recent_pulses_and_density(self, rounding: int = None) -> tuple:
        """Returns the number of pulses since this function was last called, and the same divided by the time since this function was last called.
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
            return delta_count, density
        else:
            return delta_count, round(density, rounding)
