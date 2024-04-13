from raspberry.sensors import DHT11

sensor_temperature  = DHT11.DHTClass()

while(True):
    print(sensor_temperature.read())
    pass