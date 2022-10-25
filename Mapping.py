from djitellopy import tello

import KeyPressModule as kp
import numpy as np
from time import sleep
import cv2
import math
######## PARAMETERS ##########
'''
we need the speed and we also need the angular speed 
from that we will calculate the distance and we will 
calculate how much angle do we have first we are going 
to write the forward speed 


'''
fSpeed = 117/10 # forward speed in cm/s  (15cm/s)
aSpeed = 360/10 # angular speed in degrees/s (50d/s)
interval = 0.25

dInterval = fSpeed*interval
aInterval = aSpeed*interval
##################################################
x,y = 500, 500
a = 0
yaw = 0
kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

points = [(0,0), (0.0)]

def getKeyBoardInput():
    lr, fb, ud, yv = 0, 0, 0, 0


    speed = 15
    aspeed = 50
    global x, y, yaw, a
    d = 0

    if kp.getKey("LEFT"):
        lr = -speed
        d = dInterval
        a = -180
    elif kp.getKey("RIGHT"):
        lr = -speed
        d = -dInterval
        a = 180

    if kp.getKey("UP"):
        fb = speed
        d = dInterval
        a = 270

    elif kp.getKey("DOWN"):
        fb = -speed
        d = -dInterval
        a = -90

    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("a"):
        yv = -aspeed
        yaw -= aInterval

    elif kp.getKey("d"):
        yv = aspeed
        yaw += aInterval

    if kp.getKey("q"):
        me.land()

    if kp.getKey("e"):
        me.takeoff()

    sleep(interval)
    a += yaw
    x += int(d * math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))

    return [lr, fb, ud, yv, x, y]


def drawPoints(img, points):
    '''
    in openCV we use bgr no rgb
    '''
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'({(points[-1][0]- 500)/100},{(points[-1][1]- 500)/100})m',
                (point[-1][0]+10, point[-1][1]+30), cv2.FONT_HERSHEY_PLAIN, 1,
                (255, 0, 255), 1)
while True:
    val = getKeyBoardInput()
    me.send_rc_control(val[0], val[1], val[2], val[3])

    img = np.zeros((1000, 1000, 3), np.uint8)
    if(points[-1][0] != val[4] or points[-1][1] != val[5]):
        points.append((val[4], val[5]))
    drawPoints(img, points)
    cv2.imshow("Output", img)
    cv2.waitKey(1)
   #2^8 = 256   range 0 to 255
'''
calculating a distance traveled 
example speed = 10 cm/s
time = 2s
Distance = 20 cm
(0, 20)
with angle lets say we don't go forwared all we do is rotate 
example 
Angular Speed 
45 deg/s 
time = 2s 
it means if we rotate it twice 
it will rotate one second 45 degrees 
onther 1 second it will rotate 90 degrees 
 angle = 90deg

'''


