# sht40bmp280.py

# Wrapper for using the M5STACK ENV IV environmental sensor

# local imports
from . import sht40
from . import bmp280_wrapper


def sample():
  """Sample both the sht40 and bmp280"""
  Ts, RH = sht40.get_TRH()
  Tb, P = bmp280_wrapper.get_TP()
  data = SampleData()
  data.temperature = Ts   # Use temperature reading from the SHT40
  data.humidity = RH
  data.pressure = P
  return data

class SampleData:
  """Empty class to which attributes can be added"""
  pass

if __name__ == '__main__':
  from time import sleep
  while True:
    sampledata = sample()
    print(vars(sampledata))
    print("T:", sampledata.temperature, "degC")
    print("RH:", sampledata.humidity, "%")
    print("P:", sampledata.pressure, "hPa")
    print()
    sleep(1)


