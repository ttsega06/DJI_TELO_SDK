import pygame
from djitellopy import tello

import KeyPressModule as kp
import time
import cv2
kp.init()
me = tello.Tello()
me.connect()
print(me.get_battery())
global img
me.streamon()


def getKeyBoardInput():

    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if kp.getKey("LEFT"):
        lr = -speed
    elif kp.getKey("RIGHT"):
        lr = speed

    if kp.getKey("UP"):
        fb = speed
    elif kp.getKey("DOWN"):
        fb = -speed

    if kp.getKey("w"):
        ud = speed
    elif kp.getKey("s"):
        ud = -speed

    if kp.getKey("a"):
        yv = speed

    elif kp.getKey("d"):
        yv = -speed

    if kp.getKey("q"):
        me.land();


    if kp.getKey("e"):
        me.takeoff()

    if kp.getKey('z'):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)

    return [lr, fb, ud, yv]


while True:
    val = getKeyBoardInput()
    me.send_rc_control(val[0], val[1], val[2], val[3])
    img = me.get_frame_read().frame
    # this will make the frame smaller
    img = cv2.resize(img, (360, 240))
    # this will create a window to display the result
    cv2.imshow("Image", img)

    # if we don't write this waitKey the frame will shut down
     # before we can actually see it, so we have to give it a delay of one millisecond
    cv2.waitKey(1)