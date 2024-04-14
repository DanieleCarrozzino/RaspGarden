import RPi.GPIO as GPIO
import time

class PumpClass:

    def __init__(self) -> None:
        self.PIN = 14
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN, GPIO.OUT)
        GPIO.output(self.PIN, GPIO.LOW)
        pass

    def start(self):
        GPIO.output(self.PIN, GPIO.HIGH)
        time.sleep(60*5)
        GPIO.output(self.PIN, GPIO.LOW)
        pass