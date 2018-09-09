import cv2 as cv
import numpy as np

face = cv.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

cap = cv.VideoCapture(0)

font = cv.FONT_HERSHEY_SIMPLEX

while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face.detectMultiScale(gray, 1.1, 5)

    for (x,y,w,h) in faces:
        cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
        dist = (0.6*150) / w
        dx = (x + w/2) - 320
        s = abs(dx)*0.001648*dist
        theta = (180 * np.arctan(s/dist)) / 3.14
        theta = float("{0:.2f}".format(theta))

        if dx > 0:
            cv.putText(frame, "Angle : " + str(theta) + "deg left", (x,y-25), font, 0.5, (255,255,255), 2)
        else:
            cv.putText(frame, "Angle : " + str(theta) + "deg right", (x,y-20), font, 0.5, (255,255,255), 2)

        dist = float("{0:.2f}".format(dist))
        cv.putText(frame, "Distance : " + str(dist) + "m", (x,y-10), font, 0.5, (255,255,255), 2)

    cv.imshow('Face Detection', frame)
    k = cv.waitKey(30) & 0xFF
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()
