import os
import sys
import time
from fractions import Fraction
from datetime import datetime, timedelta

import picamera
import RPi.GPIO as gp

import Accelero.Accel as accel
import GPS.gps as gps

dataFile = "gather_Data/data/"+time.strftime("%d-%m-%Y")+".txt"  #variable for data file with every day date
photosFolder = "gather_Data/photos/"+time.strftime("%d-%m-%Y")+"/"
os.system("mkdir -p gather_Data/photos/"+time.strftime("%d-%m-%Y") ) #create folder of image with every day date

CAMERA_1 = 1
CAMERA_2 = 2

def config_cameras() :
    gp.setwarnings(False)
    gp.setmode(gp.BOARD)

    gp.setup(7, gp.OUT)
    gp.setup(11, gp.OUT)
    gp.setup(12, gp.OUT)

def capture(camera, camera_number, path):
    if camera_number == CAMERA_1 :
        gp.output(7, False)
    elif camera_number == CAMERA_2 :
        gp.output(7, True)

    gp.output(11, False)
    gp.output(12, True)

    camera.capture(path)

def file_func():
    file = open(dataFile,"a+")
    file.close()
 

def gather(startHour,startMinute,finishHour,finishMinute):
    config_cameras()
    with picamera.PiCamera() as camera :
        #choose resolution of camera
        camera.resolution = [2560, 1920]
        #low light : very slow frame (1/6)(max framerate = 15)
        f = camera.framerate
        f = Fraction(1,8)
        #wait for the automatic gain control to settle
        time.sleep(2)
        #choose the exposure time
        camera.shutter_speed = camera.exposure_speed
        camera.exposure_mode = 'off'
        #100 -200 value for datetime, 400-800 value for low light
        camera.iso = 500
        #fix white balance
        g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = g
        time.sleep(0.5)

        _, _, _ ,ms= accel.auto_calibration()

        #***********take photos*****************************
        print("lets start , take photo with 1 camera",file=open(photosFolder+"output.txt","a+"))
        file_func()
        #wait until time = start time
        while not((datetime.now().time().hour == startHour) and (datetime.now().time().minute == startMinute)):
            print ("wait "+str(datetime.now().time()),file=open(photosFolder+"output.txt","a+"))
            time.sleep(30)

        #while time is different of finish time take photos
        while not((datetime.now().time().hour ==finishHour) and (datetime.now().time().minute == finishMinute )):
            capture(camera, CAMERA_1, photosFolder + time.strftime("%H:%M:%S") + ".jpg")
            print("picture 1",file=open(photosFolder+"output.txt","a+"))
            AxF, AyF, AzF,total_axes,angleX,angleY,angleZ,DxF, DyF, DzF = accel.gatherDistance(ms)
            Latitude,Longitude= gps.getGPSvalue()
            file = open(dataFile,"a+")
            file.write("{},{};{};{},{},{};{};{},{};{};{},{};{} \n".format(time.strftime("%H:%M:%S"),AxF,AyF,AzF,total_axes,angleX,angleY,angleZ,DxF,DyF,DzF,Latitude,Longitude))
            file.close() 
                
    print("End",file=open(photosFolder+"output.txt","a+"))
