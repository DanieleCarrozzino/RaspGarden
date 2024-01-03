# sudo pip3 install Adafruit_DHT
import Adafruit_DHT

class DHTClass:

    #sensor = Adafruit_DHT.DHT11

    def __init__(self) -> None:
        self.sensor = Adafruit_DHT.DHT11
        self.pin    = 4 

    def read(self):
        print("Statrt read") 
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        print(f"humidity : {humidity} | temperature : {temperature}")
        pass

    pass