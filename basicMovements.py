from djitellopy import tello
from time import sleep

me = tello.Tello()
me.connect()

print(me.get_battery())

me.takeoff()
# sending command
me.send_rc_control(0, 50, 0, 0)
# sleep
sleep(2)
'''
Us you saw the drone first took off it want forward for two second 
then it want towrd the right side for two seconds and then it landed 
if do -30 insted it will go tword the left, we right on the code on the obed -50
it will go backwards, thats the basic idea if we want to rotate we can write 30 on 4th index and zero in the first index
that's we can go upword forward and down ward that way we can control the yaw  


'''
me.send_rc_control(30, 0, 0, 0)
sleep(2)
# if we don't do that conde the drone will go forward when it is landing
# this line of conde will stop it completly then we will ask it to land
me.send_rc_control(0, 0, 0, 0)
# land
me.land()

'''
as you see it want of and go forward in two second at the speed of 50 it landed 


'''