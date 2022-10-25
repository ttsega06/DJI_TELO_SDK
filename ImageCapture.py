import img as img
from djitellopy import tello
# this will help us to process the image faster

import cv2

me = tello.Tello()
me.connect()

print(me.get_battery())

me.streamon()

while True:
    img = me.get_frame_read().frame
    # this will make the frame smaller
    img = cv2.resize(img, (360, 240))
    # this will create a window to display the result
    cv2.imshow("Image", img)

    # if we don't write this waitKey the frame will shut down
    # before we can actually see it, so we have to give it a delay of one millisecond
    cv2.waitKey(1)

'''
we are going to use the keyboard to actually fly the drone. To do this we need to get the command of the keyboard
 first then we can implment weith our basic movments, we can run them together 
  to do this we are going to create a new modul called keypress module 
  a modul is basically a piece of code that can run individually  


'''


