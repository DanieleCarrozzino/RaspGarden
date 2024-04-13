from raspberry.sensors import DHT11
from raspberry.sensors import ADS1115
import time

sensor_moisture     = ADS1115.ADS1115Class()

while(True):
    print(sensor_moisture.read())
    time.sleep(1)
    pass