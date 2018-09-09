import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.OUT)

p = GPIO.PWM(12, 50)

angle = input("Enter Angle : ")

p.start(2.5)
p.ChangeDutyCycle(angle)
time.sleep(1)
GPIO.cleanup()

#try:
#    while True:
#        p.ChangeDutyCycle(7.5)  # turn towards 90 degree
#        time.sleep(1) # sleep 1 second
#        p.ChangeDutyCycle(2.5)  # turn towards 0 degree
#        time.sleep(1) # sleep 1 second
#        p.ChangeDutyCycle(12.5) # turn towards 180 degree
#        time.sleep(1) # sleep 1 second
#except KeyboardInterrupt:
#    p.stop()
#    GPIO.cleanup()
