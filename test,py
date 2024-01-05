import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create ADC object
ads = ADS.ADS1115(i2c)

# Create analog input channels
chan = AnalogIn(ads, ADS.P0)  # Change ADS.P0 to ADS.P1 for AIN1, ADS.P2 for AIN2, etc.

# Read analog input continuously
while True:
    print("Voltage: {:.2f}V".format(chan.voltage))
    print("ADC Value: {}".format(chan.value))
    time.sleep(1)
