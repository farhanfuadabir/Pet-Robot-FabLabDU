import cv2 as cv
import numpy as np
import RPi.GPIO as GPIO
import time as tm

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)

p = GPIO.PWM(32, 100)
p.start(0)

def forward():
    p.ChangeDutyCycle(25)
    GPIO.output(11, True)
    GPIO.output(13, False)
    GPIO.output(16, True)
    GPIO.output(18, False)

def right():
    p.ChangeDutyCycle(15)
    GPIO.output(11, True)
    GPIO.output(13, False)
    GPIO.output(16, False)
    GPIO.output(18, True)

def left():
    p.ChangeDutyCycle(15)
    GPIO.output(11, False)
    GPIO.output(13, True)
    GPIO.output(16, True)
    GPIO.output(18, False)

def halt():
    p.ChangeDutyCycle(25)
    GPIO.output(11, False)
    GPIO.output(13, False)
    GPIO.output(16, False)
    GPIO.output(18, False)

font = cv.FONT_HERSHEY_SIMPLEX

lower = (10, 170, 100)
upper = (20, 255, 255)

cap = cv.VideoCapture(0)
ret, frame = cap.read()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv.resize(frame, (240, 144), interpolation = cv.INTER_LINEAR)

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower, upper)
    cnts = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv.contourArea)
        ((x, y), radius) = cv.minEnclosingCircle(c)
        M = cv.moments(c)
        if M["m00"] != 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 10:
            #cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            #cv.circle(frame, center, 5, (0, 0, 255), -1)
            #dist = (0.25*140) / (radius*2)
            dist = (0.25*52.5) / (radius*2)

            dx = x - 120
            s = abs(dx)*0.001648*dist
            theta = (180 * np.arctan(s/dist)) / 3.14
            theta = float("{0:.2f}".format(theta))
            print(theta)

            if dx > 0:
                #cv.putText(frame, "Angle : " + str(theta) + "deg left", center, font, 0.5, (255,255,255), 2)
                if theta > 15:
                   right()
                   #print("right");
            else:
                #cv.putText(frame, "Angle : " + str(theta) + "deg right", center, font, 0.5, (255,255,255), 2)
                if theta > 15:
                   left()
                   #print("left");

            # dist = float("{0:.2f}".format(dist))
            # cv.putText(frame, "Distance : " + str(dist) + "m", (center[0], center[1] - 20), font, 0.5, (255,255,255), 2)

    #cv.imshow("Frame", frame)

    k = cv.waitKey(30) & 0xFF
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()
