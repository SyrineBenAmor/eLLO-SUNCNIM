import numpy as np
import cv2
import time
from datetime import datetime, timedelta
import sys

sys.path.append('gather_Data')
import gatherData

sys.path.append('gather_Data/Accelero/')
import Accel

sys.path.append('gather_Data/GPS/')
import gps

sys.path.append('find_crack_in_map/')
import displayData as location
import plan
from plan import pinMap

sys.path.append('Image_processing/')
import Crack_Detection as detection


then = time.time()
planSite ="find_crack_in_map/Prototype vue de Haut.jpg"

pathImage = "Image_processing/image_processing_output/"+time.strftime("%d-%m-%Y")+"fissure/"+"*.jpg"
nameDatafile = "gather_Data/data/"+time.strftime("%d-%m-%Y")+".txt"

startHour   = 10
startMinute = 21
finishHour  = 10
finishMinute = 59

#*************************************************************************
def main():
    #gatherData.gatherData(startHour,startMinute,finishHour,finishMinute)#gather data until Time cleaning finish
    while not((datetime.now().time().hour > finishHour) and (datetime.now().time().minute > finishMinute)): #if time cleaning finish
        detection.detectcrack()# treat image and stock them in other folder(caisson folder, fissure folder,ligne de separation folder)
        location.displayData(nameDatafile,pathImage)#display acceleration, longitude and lattitude
    """
    realCoordinate = (7,1)
    siteMap = pinMap(planSite)
    
    image = siteMap.brokenMirrors(realCoordinate)
    cv2.imshow("Image with red caisson ", image)
    
    print("Execution Time = "+str(float(time.time() - then)) + " s")
    """
    #********************close condition*************************************

    k = cv2.waitKey(0)
    if k == 27: #wait for ESC key to exit
        cv2.destroyAllWindows()
    print ('end')
    
if __name__== "__main__":
    main()
    
