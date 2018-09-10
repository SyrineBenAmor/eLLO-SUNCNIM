import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt


import syrineLib as syrine

global path
path = "crack.jpg"
crackedMiror = []
#**********************************************************


def detectcrack():
    i=0
    for imagePath in glob.glob(path):
        i+=1
        gray = syrine.loadImage(imagePath)  #Load a single imge  
        mean = int(gray.mean())    
        #print("mean = " ,str(mean))
        thresh = syrine.threshold(gray,"triangle")     # binarization of the loaded image
        syrine.show('Binarized Image '+str(i),thresh)
        alpha = 3.0
        beta= 0
        contrast = syrine.contrast(gray, alpha, beta)
        #syrine.show('Contrast', contrast)
        outContrast,state = syrine.processImage(gray, contrast, thresh)
        if state == "separation" :
            thresh = syrine.threshold(gray,"binary")
            outContrastBis,state = syrine.processImage(gray, contrast, thresh)
            if state != "caisson" :
                syrine.show('rectangle '+str(i),outContrast)
            else :
                syrine.show('rectangle '+str(i),outContrastBis)
        else :
            syrine.show('rectangle '+str(i),outContrast)
            crackedMiror.append(imagePath)
            
        return (crackedMiror)

