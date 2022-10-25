'''
to track a particular a object or a face or even a full body
we will do it with face tracking but later on you can implement it with any of the
other object as well
when we have to move the drone and we have to track our face
we need two different thing we need the motion of forward and backward
and we need the motion of rotation so we need yaw and forward and backwards
lets see forward and backwords first so we will treat both of these individually
and then we will combine the code for them
if the object or the face looking small then it means we need to move forward
if the object or the face looking quite big then we need to move backwards
so we are to close we need to go back
the read are will show as where the drone is to clos eor to far from the object
green region is where we do not have to move at all
lets say the person moved backward so the drone will have to compensate and it will move forward
it will go until the green zone and it will stop
lets say she moved forward then the drown should counter the movement by going back
it have to go back until it reachs the green zone

Yaw Angle
The idea here is that we are able to go forward and backwards but what if the person start rotating
The idea here is that we always want our object to be center of the image so lets say this frame is the image
that we have and the person is not in the middle then if thier in the left side we will move the drone
we will rotate and that will bring the person in the center
again if the person moved we have to rotate the drone to bring the person to the center
lets say our object is on the left hand side so we will say rotate anti-clockwise direction
with the speed of 20, so it will start moving at the speed of 20 when it reachs the center
it can't stop immediately it will move a little bit forward becosue of the momentum
we can meake it better by reducing the speed as we reach our destination
lets say the speed is 20 once we are getting closer lets say the person is on the left
then we will raduce the speed lets say right now is 10 then it will become 5 by the time
it reachs to the center it becomes 0.
'''
import time

import cv2
import faces as faces
import numpy as np
import img as img
from djitellopy import tello
# this will help us to process the image faster



me = tello.Tello()
me.connect()

print(me.get_battery())

me.streamon()
me.takeoff()
me.send_rc_control(0, 0, 25, 0)
time.sleep(2,2)


w, h = 360, 240
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError = 0

def findFace(img):

    faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

    myFaceListC = []
    myFaceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)

    if len(myFaceListArea)!= 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]


def trackFace(info, w, pid, pError):
    area = info[1]
    x,y = info[0]
    fb = 0

    error = x - w // 2
    speed = pid[0] * error + pid[1] * (error-pError)
    speed = int(np.clip(speed, -100, 100))


    if area >fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20
    if x==0:
        speed = 0
        error = 0

    # print(speed, fb)

    me.send_rc_control(0, fb, 0, speed)
    return error


# cap = cv2.VideoCapture(1)
while True:
    # _, img = cap.read()
    img = me.get_frame_read().frame
    img = cv2.resize(img, (w, h))
    img, info = findFace(img)
    pError = trackFace(info, w, pid, pError)
    # print("Center", info[1], "Area", info[1])

    cv2.imshow("Output", img)
    if cv2.waitkey(1) & 0xFF == ord('q'):
        me.land()
        break