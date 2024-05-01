# sht40bmp280.py

# Wrapper for using the M5STACK ENV IV environmental sensor

# local imports
from . import sht40
from . import bmp280_wrapper


def sample():
  """Sample both the sht40 and bmp280"""
  Ts, RH = sht40.get_TRH()
  Tb, P = bmp280_wrapper.get_TP()

  data = dict()
  data['temperature'] = Ts   # Use temperature reading from the SHT40, discard temperature reading from BMP280
  data['humidity'] = RH
  data['pressure'] = P

  return data

# Test if run directly. Beware import paths may break. 
if __name__ == '__main__':
  from time import sleep
  while True:
    sampledata = sample()
    print(sampledata)
    print("T:", sampledata['temperature'], "degC")
    print("RH:", sampledata['humidity'], "%")
    print("P:", sampledata['pressure'], "hPa")
    print()
    sleep(1)


