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
    crackedMiror = crack.detectcrack()
    print("list of name for all image which has cracks \n",crackedMiror) 
    
    planMasked = plan.filter(planSite)
    cv2.imshow("Mask Applied", planMasked)

    planWithContours, contours = plan.drawContoursOfMiror (planMasked,planSite)
    print ("total caisson in site ( 14 lignes * 8 caissons = ",len(contours) )
    cv2.imshow('contours',planWithContours)
    
    
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
    
