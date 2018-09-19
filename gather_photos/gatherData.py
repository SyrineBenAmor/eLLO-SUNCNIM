import picamera
import time
from fractions import Fraction
from datetime import datetime, timedelta
import os

import Accel
import gps

startHour   = 11
startMinute = 21
finishHour  = 12
finishMinute = 20

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
    #***********take photos*****************************


        print("lets start")
        #wait until time = start time
        while not((datetime.now().time().hour == startHour) and (datetime.now().time().minute == startMinute)):
            print ("wait "+str(datetime.now().time()))
            time.sleep(30)
        os.system("mkdir /home/pi/Desktop/eLLO-SUNCNIM/gather_photos/test."+time.strftime("%d-%m-%Y"))
        print("Folder Created")
        file = open(time.strftime("%d-%m-%Y")+"Data.txt","a+")
        file.write("Time(s), AngleX(°); AngleY(°);AngleZ(°), DistanceX[mm];DistanceY[mm];DistanceZ[mm], AccelX[mm/s^2];AccelY[mm/s^2];AccelZ[mm/s^2], Latitude Longitude\n")
        file.close()

        #while time is different of finish time take photos
        while not((datetime.now().time().hour == finishHour) and (datetime.now().time().minute == finishMinute)):
            
            camera.capture_sequence(["/home/pi/Desktop/eLLO-SUNCNIM/gather_photos/test."+time.strftime("%d-%m-%Y")+"/"+"img"+time.strftime("%H:%M:%S")+".jpg"])
            print ("picture")
            _, _, _ ,ms= Accel.auto_calibration()
            DxF,DyF,DzF = Accel.gatherDistance(ms)
            #Lat,long= gps.getGPSvalue()
            
            
        print('End')

        k = cv2.waitKey(0)
        if k == 27: #wait for ESC key to exit
            cv2.destroyAllWindows()
        print ('end')
        
if __name__== "__main__":
    main(startHour,startMinute,finishHour,finishMinute)    
