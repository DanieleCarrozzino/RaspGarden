from raspberry.water import Pump
import time

pump = Pump.PumpClass()

while(True):
    pump.start()
    time.sleep(100)
    pass