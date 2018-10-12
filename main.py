import numpy as np
import cv2
import time
import sys

sys.path.append('gather_Data/Accelero/')
import Accel

sys.path.append('gather_Data/GPS/')
sys.path.append('find_crack_in_map/')
import plan
from plan import pinMap

sys.path.append('Image_processing/')
import Crack_Detection as detection

then = time.time()
planSite ="find_crack_in_map/Prototype vue de Haut.jpg"

#*************************************************************************
def main():
    detection.detectcrack()
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
    
