import numpy as np
import cv2
import time

import sys

sys.path.append('Accelero/')
import Accel

sys.path.append('GPS/')
import plan

sys.path.append('Image_processing/')
import Crack_Detection as detection

then = time.time()
planSite ="GPS/Prototype vue de Haut.jpg"

#*************************************************************************
def main():
    crackedMiror = detection.detectcrack()
    print("list of name for all image which has cracks \n",crackedMiror) 
    
    planMasked = plan.filter(planSite)
    cv2.imshow("Mask Applied", planMasked)

    listOfCaisson = plan.listOfCaisson(planMasked)
    #print(plan.origin(planMasked))
    
    print ("total caisson in site ( 14 lignes * 8 caissons = ",len(listOfCaisson) )
    #cv2.imshow('contours',planWithContours)

    coordinate_origin = plan.origin(planMasked)
    print("coordonnees (x,y) du nouveau origine = ",coordinate_origin)
    
    realCoordinate = (80,18)
    image,coordinateInpixel = plan.convertRealCoordinateToPixel(planSite,realCoordinate)
    print("coordinate in pixels=",coordinateInpixel) 
    cv2.imshow("line",image)
    
    contour = plan.findCaisson(coordinateInpixel, listOfCaisson)
    
    imageWithColored_Caisson=plan.colorCaisson(planSite,contour)
    cv2.imshow("image colore",imageWithColored_Caisson)
  
    print("Execution Time = "+str(float(time.time() - then)) + " s")
    '''
    total_axes = Accel.getAcceleration()
    print("sum of the 3 axes = ",total_axes)
    
    distance_total = Accel.calculateDistance (total_axes)
    print ("total distance = ",ditance_total)
    '''
    #********************close condition*************************************

    k = cv2.waitKey(0)
    if k == 27: #wait for ESC key to exit
        cv2.destroyAllWindows()
    print ('end')
    
if __name__== "__main__":
    main()
    
