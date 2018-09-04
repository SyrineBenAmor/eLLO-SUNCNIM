import numpy as np
import cv2
import time

import sys

sys.path.append('Accelero/')
import Accel

sys.path.append('GPS/')
import plan

sys.path.append('Image_processing/')
import Crack_Detection as crack

then = time.time()
planSite ="GPS/Prototype vue de Haut.jpg"

#*************************************************************************
def main():
    crackedMiror = detection.detectcrack()
    print("list of name for all image which has cracks \n",crackedMiror) 
    
    planMasked = plan.filter(planSite)
    cv2.imshow("Mask Applied", planMasked)

    listOfContours = plan.listOfContours(planMasked)
    #print(plan.origin(planMasked))
    
    print ("total caisson in site ( 14 lignes * 8 caissons = ",len(listOfContours) )
    #cv2.imshow('contours',planWithContours)

    coordinate_origin = plan.origin(planMasked)
    print("coordonnees (x,y) du nouveau origine = ",coordinate_origin)
    
    
    contour = plan.statePoint(coordinate_origin, listOfContours)
    
    imageWithColored_Contour=plan.changeColorInsideContour(planSite,contour)
    cv2.imshow("image colore",imageWithColored_Contour)
    
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
    
