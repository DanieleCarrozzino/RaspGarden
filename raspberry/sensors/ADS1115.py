import Adafruit_ADS1x15

class ADS1115Class:

    def __init__(self) -> None:
        self.adc    = Adafruit_ADS1x15.ADS1115()
        self.GAIN   = 1 

    #
    # Read (main function)
    #
    # read the value of the 4 sensors from
    # an ADC ADS1115, return an array of 4 values
    # min 4000 max 16000
    #
    def read(self):

        values = [0]*4
        try:
            for i in range(4):
                # Read the specified ADC channel using the previously set gain value.
                values[i] = self.adc.read_adc(i, gain=self.GAIN)
            print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
            print(values)
        except:
            print("Exception catched")

        return values
