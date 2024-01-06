# sudo pip3 install Adafruit_DHT
import Adafruit_DHT
import time

class DHTClass:

    def __init__(self) -> None:
        self.sensor = Adafruit_DHT.DHT11
        self.pin    = 4 

    #
    # Read humidity and temperature
    # return the avarage value of 
    # the last 3 valid mesaurament
    # 
    def read(self):
        print("Start reading temperature and humidity...") 

        valid_result_count      = 0
        invalid_result_count    = 0
        avarage_tempreature     = 0
        avarage_humidity        = 0
        got_exception           = False

        while valid_result_count < 3 and not got_exception:
            print(valid_result_count)
            try:
                humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
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
                    time.sleep(2)

                print(f"humidity : {humidity} | temperature : {temperature}")
                pass
            except:
                print("Get an exception while reading the temperature and humidity sensor")
                got_exception = True
                pass
            pass
        return avarage_tempreature, avarage_humidity
    pass