# encoderwheel.py

# imports
from gpiozero import RotaryEncoder


class EncoderWheel():

    def __init__(self, Apin, Bpin, steps_per_rev, circ=None, dia=None):
        """Uses gpiozero.RotaryEncoder. Specify either circ or dia."""
        self.encoder = RotaryEncoder(Apin, Bpin, max_steps=0)
        self.steps_per_rev = steps_per_rev

        if circ is None:
            if dia is None:
                raise TypeError("Either wheel circumference or diameter needs to be specified!")
            else:
                self.circ = 3.14159265359*dia
        else:
            self.circ = circ

    def __call__(self):
        """Return the current displacement of the wheel, in the units of circ or dia supplied."""
        dist = self.circ*self.encoder.steps/self.steps_per_rev
        return round(dist,3)

    # position can be reset with .encoder.steps = 0 , no wrapper needed.
