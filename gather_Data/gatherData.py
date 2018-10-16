import picamera
import time
from fractions import Fraction
from datetime import datetime, timedelta
import os
import sys

import Accelero.Accel as accel
import GPS.gps as gps


def gatherData(startHour,startMinute,finishHour,finishMinute):
    with picamera.PiCamera() as camera :
    #************fix the values to take photos with same terms of brightness
        #choose resolutionof camera (camera type 2)
        camera.resolution = (2560, 1920)
        #low light : very slow framerate (1/6) (Max framerate = 15 )
        f= camera.framerate
        f= Fraction(1 ,8)
        #wait for the automatic gain control to settle
        time.sleep(2)
        #choose the exposure time
        camera.shutter_speed = camera.exposure_speed
        camera.exposure_mode = 'off'
        # 100-200 value for daytime,, 400-800 value for low light
        camera.iso = 500
        #fix white balance
        g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = g
        #wait 1sec
        time.sleep(0.5)
        _, _, _ ,ms= accel.auto_calibration()
    #***********take photos*****************************


        print("lets start")
        #wait until time = start time
        while not((datetime.now().time().hour == startHour) and (datetime.now().time().minute == startMinute)):
            print ("wait "+str(datetime.now().time()))
            time.sleep(30)
        dataFile = "gather_Data/data/"+time.strftime("%d-%m-%Y")+".txt"  #variable for data file with every day date
        photosFolder = "gather_Data/photos/"+time.strftime("%d-%m-%Y")
        os.system("mkdir gather_Data/photos/"+time.strftime("%d-%m-%Y") ) #create folder of image with every day date  
        file = open(dataFile,"a+")
        file.write("Time,AccelX[mm/s^2];AccelY[mm/s^2];AccelZ[mm/s^2],Total_axes acceleration, AngleX(deg); AngleY(deg);AngleZ(deg), DistanceX[mm];DistanceY[mm];DistanceZ[mm], Latitude ;Longitude\n")
        file.close()

        #while time is different of finish time take photos
        while not((datetime.now().time().hour == finishHour) and (datetime.now().time().minute == finishMinute)):
            
            camera.capture_sequence([photosFolder+"/"+time.strftime("%H:%M:%S")+".jpg"])
            print ("picture")
            
            AxF, AyF, AzF,total_axes,angleX,angleY,angleZ,DxF, DyF, DzF = accel.gatherDistance(ms)
            #Latitude,Longitude= gps.getGPSvalue()
            file = open(dataFile,"a+")
            file.write("{},{};{};{},{},{};{};{},{};{};{}\n".format(time.strftime("%H:%M:%S"),AxF,AyF,AzF,total_axes,angleX,angleY,angleZ,DxF,DyF,DzF))
            file.close() 
            
        print('End')