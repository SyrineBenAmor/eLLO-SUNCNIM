import picamera
import time
from fractions import Fraction
from datetime import datetime, timedelta
import os


startHour   = 15
startMinute = 25
finishHour  = 15
finishMinute = 59


import Accel
import gps

with picamera.PiCamera() as camera :
    #************fix the values to take photos with same terms of brightness
    #choose resolutionof camera (camera type 2)
    camera.resolution = (2560, 1920)
    #low light : very slow framerate (1/6) (Max framerate = 15 )
    f= camera.framerate
    f= Fraction(1 ,8)
    #wait for the automatic gain control to settle
    #time.sleep(2)
    #choose the exposure time
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    # 100-200 value for daytime,, 400-800 value for low light
    camera.iso = 500
    #fix white balance
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    #wait 2sec
    #time.sleep(2)
        
    #***********take photos*****************************

    print("lets start")
    #wait until time = start time
    while not((datetime.now().time().hour == startHour) and (datetime.now().time().minute == startMinute)):
        print ("wait "+str(datetime.now().time()))
        time.sleep(30)
    os.system("mkdir /home/pi/Desktop/eLLO-SUNCNIM/gather_photos/test."+time.strftime("%d-%m-%Y"))
    print("Folder Created")
    #while time is different of finish time take photos
    while not((datetime.now().time().hour == finishHour) and (datetime.now().time().minute == finishMinute)):
        print ("time pour prendre une photo",datetime.now().time())
        camera.capture_sequence(["/home/pi/Desktop/eLLO-SUNCNIM/gather_photos/test."+time.strftime("%d-%m-%Y")+"/"+"img"+time.strftime("%H:%M:%S")+".jpg"])
        
        _, _, _ ,ms= Accel.auto_calibration()
        DxF,DyF,DzF = Accel.gatherDistance(ms)
        Lat,long= gps.getGPSvalue()
        #time.sleep(2) #wait 2 sec
        print ("picture")
    print('End')

