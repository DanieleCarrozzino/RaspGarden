# sudo pip3 install Adafruit_DHT
import Adafruit_DHT
import time

from utility import Logger 

# Configurazione guardando il blu
# pin centrale attaccato a 5V
# pin a destra al ground
# pin a Sinistra al pin GPIO4
class DHTClass:

    def __init__(self) -> None:
        #Utility
        self.logger = Logger.logger()
        self.sensor = Adafruit_DHT.DHT11
        self.pin    = 4 

    #
    # Read humidity and temperature
    # return the avarage value of 
    # the last 3 valid mesaurament
    # 
    def read(self):
        valid_result_count      = 0
        invalid_result_count    = 0
        avarage_tempreature     = 0
        avarage_humidity        = 0
        got_exception           = False

        while valid_result_count < 3 and not got_exception:
            try:
                humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
                self.logger.d("internal temperature")
                self.logger.d(temperature)
                if humidity != None and temperature != None:
                    valid_result_count  =  valid_result_count + 1
                    avarage_tempreature = avarage_tempreature + temperature
                    avarage_humidity    = avarage_humidity + humidity
                else:
                    # Avoid infinite loop over this sensor
                    invalid_result_count += 1

                    # TODO increase threshold
                    if invalid_result_count > 1:
                        return 0, 0

                    # Get more time to wake up the sensor
                    time.sleep(1)
                pass
            except Exception as e:
                got_exception = True
                self.logger.d(e)
                pass
            pass
        return avarage_tempreature / valid_result_count, avarage_humidity / valid_result_count
    pass