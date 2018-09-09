import RPi.GPIO as GPIO
import time as tm

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.OUT)

while(True):
     GPIO.output(37, True)
     tm.sleep(1)
     GPIO.output(37, False)
     tm.sleep(1)

GPIO.cleanup()
