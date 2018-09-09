import Rpi.GPIO as GPIO
import time as tm

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(39, GPIO.OUT)

while(True):
     GPIO.output(39, True)
     tm.sleep(1)
     GPIO.output(19, False)
     tm.sleep(1)

 GPIO.cleanup()
