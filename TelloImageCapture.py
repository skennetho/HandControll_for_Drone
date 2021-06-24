#tello Image Capture 

from djitellopy import tello
from time import sleep
import HandTrackingModule as htm
import cv2

me = tello.Tello()
me.connect()
me.streamon()
print(me.get_battery())

detector = htm.handDetector()
WINDOW_H = 600
WINDOW_W = 900
center_margin = 100

me.takeoff()

while True:
    img = me.get_frame_read().frame
    img = cv2.resize(img, (WINDOW_W,WINDOW_H))
    
    img =detector.findHands(img)
    lmList, bbox = detector.findPosition(img,draw=False)
    handDirection =0
    
    #hand detected
    if lmList:
        handDirection = detector.findPointingDirection(img)
        print('hand detecting...',handDirection,',',htm.DIR[handDirection])
        #make hand center
        bbox_center_x = (bbox[0] + bbox[2])/2
        if(bbox_center_x<WINDOW_W/2-center_margin):
            print('hand location', bbox_center_x,'right')
            me.send_rc_control(0,0,0,-30)
        elif(bbox_center_x>WINDOW_W/2+center_margin):
            print('hand location', bbox_center_x,'left')
            me.send_rc_control(0,0,0,30)
        else:
            print('hand location', bbox_center_x)
            #me.send_rc_control(0,0,0,0)
    
    control = htm.DIR[handDirection]
    if control == "HOLD":
        me.send_rc_control(0,0,0,0)
    elif control == "FRONT":
        me.send_rc_control(0,20,0,0)
    elif control == "LEFT":
        me.send_rc_control(30,0,0,0)
    elif control == "RIGHT":
        me.send_rc_control(-30,0,0,0)
    elif control == "UP":
        me.send_rc_control(0,0,20,0)
        #me.takeoff()                #(0,0,20,0)
    elif control == "DOWN":
        me.send_rc_control(0,0,-25,0)
        #me.land()                   #(0,0,-20,0)
    elif control == "BACK":
        me.send_rc_control(0,-20,0,0)
    
    cv2.imshow("tello view", img)
    cv2.waitKey(1)
    
    
    
