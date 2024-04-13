from raspberry.sensors import DHT11
from raspberry.sensors import ADS1115

sensor_temperature  = DHT11.DHTClass()
sensor_moisture     = ADS1115.ADS1115Class()

while(True):
    print(sensor_temperature.read())
    print(sensor_moisture.read())
    pass