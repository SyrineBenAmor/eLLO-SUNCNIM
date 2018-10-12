import picamera
import time
from fractions import Fraction
from datetime import datetime, timedelta
import os
import sys

import Accelero.Accel as accel
import GPS.gps as gps

startHour   = 10 
startMinute = 17
finishHour  = 10
finishMinute = 59

def main(startHour,startMinute,finishHour,finishMinute):
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
        dataFile = "gather_Data/data/"+time.strftime("%d-%m-%y")+".txt"  #variable for data file with every day date
        photosFolder = "gather_Data/photos/"+time.strftime("%d-%m-%y")   
        os.system("mkdir gather_Data/photos/"+time.strftime("%d-%m-%y") ) #create folder of image with every day date
        file = open(dataFile,"a+")
        file.write("Time(s),AccelX[mm/s^2];AccelY[mm/s^2];AccelZ[mm/s^2], AngleX(deg); AngleY(deg);AngleZ(deg), DistanceX[mm];DistanceY[mm];DistanceZ[mm], Latitude ;Longitude\n")
        file.close()

        #while time is different of finish time take photos
        while not((datetime.now().time().hour == finishHour) and (datetime.now().time().minute == finishMinute)):
            
            camera.capture_sequence([photosFolder+"/"+time.strftime("%H:%M:%S")+".jpg"])
            print ("picture")
            
            AxF, AyF, AzF,angleX,angleY,angleZ,DxF, DyF, DzF = accel.gatherDistance(ms)
            #Latitude,Longitude= gps.getGPSvalue()
            file = open(dataFile,"a+")
            file.write("{},{};{};{},{};{};{},{};{};{}\n".format(int(time.time()),AxF,AyF,AzF,angleX,angleY,angleZ,DxF,DyF,DzF))
            file.close() 
            
        print('End')

        k = cv2.waitKey(0)
        if k == 27: #wait for ESC key to exit
            cv2.destroyAllWindows()
        print ('end')
        
if __name__== "__main__":
    main(startHour,startMinute,finishHour,finishMinute)    
