import cv2 as cv
import numpy as np

body = cv.CascadeClassifier('haarcascades/haarcascade_fullbody.xml')

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    bodies = body.detectMultiScale(gray, 1.1, 5)
    for (x,y,w,h) in bodies:
        cv.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)

    cv.imshow('Body Detection', frame)
    k = cv.waitKey(30) & 0xFF
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()
