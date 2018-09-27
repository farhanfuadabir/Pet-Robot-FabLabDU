import cv2 as cv
import numpy as np
import threading

font = cv.FONT_HERSHEY_SIMPLEX
cap = cv.VideoCapture(0)

lower = (10, 170, 100)
upper = (20, 255, 255)

lower = (10, 170, 100)
upper = (20, 255, 255)

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
            cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv.circle(frame, center, 5, (0, 0, 255), -1)
            dist = (0.25*140) / (radius*2)
            dx = (x + radius) - 120
            s = abs(dx)*0.001648*dist
            theta = (180 * np.arctan(s/dist)) / 3.14
            theta = float("{0:.2f}".format(theta))
            print(theta)
            if dx > 0:
                cv.putText(frame, "Angle : " + str(theta) + "deg left", center, font, 0.5, (255,255,255), 2)
            else:
                cv.putText(frame, "Angle : " + str(theta) + "deg right", center, font, 0.5, (255,255,255), 2)

            dist = float("{0:.2f}".format(dist))
            cv.putText(frame, "Distance : " + str(dist) + "m", (center[0], center[1] - 20), font, 0.5, (255,255,255), 2)

    cv.imshow("Frame", frame)

    k = cv.waitKey(30) & 0xFF
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()
