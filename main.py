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
import displayData
from displayData import fetchData 
import plan
from plan import pinMap

sys.path.append('Image_processing/')
import Crack_Detection as detection


then = time.time()
planSite ="find_crack_in_map/Prototype vue de Haut.jpg"

pathImage = "Image_processing/image_processing_output/"+time.strftime("%d-%m-%Y")+"/fissure/*.jpg"
pathDatafile = "gather_Data/data/"+time.strftime("%d-%m-%Y")+".txt"

startHour1   = 11
startMinute1 = 52
finishHour1  = 11
finishMinute1 = 53

startHour2   = 11
startMinute2 = 55
finishHour2  = 11
finishMinute2 = 56

#**************************************Principal program***********************************
def main():
    
    gatherData.gatherData(startHour1,startMinute1,finishHour1,finishMinute1)#gather data until Time cleaning finish
    gatherData.gatherData(startHour2,startMinute2,finishHour2,finishMinute2)#gather data until Time cleaning finish
    """
    detection.detectcrack()# treat image and stock them in other folder(caisson folder, fissure folder,ligne de separation folder)
    gpsDataOfcrackedMiror = fetchData(pathImage,pathDatafile)#create instance of the class that display acceleration, longitude and lattitude
    gpsDataArray = gpsDataOfcrackedMiror.gpsDataCouple() #stock gps data coordinate of all cracked miror in an array
    print(gpsDataArray)
    
    siteMap = pinMap(planSite) #create instance of the class that recolor all damaged "caisson" coordinates using GPS coordinate sotcked in the array "gpsDataArray"
    for i in range (0,len(gpsDataArray)): #
        print(gpsDataArray[i])
        image = siteMap.brokenMirrors(gpsDataArray[i])
    cv2.imshow("Image with red caisson ", image)
    cv2.imwrite("Image_processing/image_processing_output/"+time.strftime("Plan %d-%m-%Y")+".jpg",image)
    cv2.imwrite("/var/www/html/img/Fresnel.jpg",image)
    """
    print("Execution Time = "+str(float(time.time() - then)) + " s")
    sys.exit()
    #********************close condition*************************************

    k = cv2.waitKey(0)
    if k == 27: #wait for ESC key to exit
        cv2.destroyAllWindows()
    print ('end')
    
if __name__== "__main__":
    main()
    
