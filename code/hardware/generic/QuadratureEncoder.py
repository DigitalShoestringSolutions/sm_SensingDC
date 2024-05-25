# QuadratureEncoder.py

# installed imports
from gpiozero import RotaryEncoder


class EncoderWheel():

    def __init__(self, Apin, Bpin, steps_per_rev, circ=None, dia=None):
        """Uses gpiozero.RotaryEncoder. Specify either circ or dia."""
        self.encoder = RotaryEncoder(Apin, Bpin, max_steps=0)
        self._steps_per_rev = steps_per_rev

        if circ is None:
            if dia is None:
                raise TypeError("Either wheel circumference or diameter needs to be specified!")
            else:
                self._circ = 3.14159265359*dia
        else:
            self._circ = circ

    def __call__(self, rounding=3):
        return self.get_current_position(rounding)

    def get_current_position(self, rounding=None):
        """Return the current tangential displacement of the wheel, in the units of circ or dia supplied.
        rounding should be either None or an int of decimal places.
        Position can be reset with .encoder.steps = 0, no wrapper needed
        """

        dist = self._circ*self.encoder.steps/self._steps_per_rev

        if rounding is None:
            return dist
        else:
            return round(dist, rounding)
