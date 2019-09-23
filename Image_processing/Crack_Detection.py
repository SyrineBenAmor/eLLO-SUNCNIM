import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import time
import os

import syrineLib as syrine

SEPARATION = "SEPARATION"
CRACK = "CRACK"
CAISSON = "CAISSON"
OTHERS = "OTHERS"

#**********************************************************


def detectcrack(path):
    i=0
    #create new folder every day which name is the date into image_processing_output folder 
    newFolderEveryDay = "Image_processing/image_processing_output/"+time.strftime("%d-%m-%Y")
    if not os.path.exists(newFolderEveryDay):
        os.makedirs(newFolderEveryDay)
    #create 3 folders for caisson ,separation and fissure
    folderCaisson    =  newFolderEveryDay+"/caisson"
    folderSeparation =  newFolderEveryDay+"/separation"
    folderFissure    =  newFolderEveryDay+"/fissure"
    folderOthers     =  newFolderEveryDay+"/others"
    if not os.path.exists(folderCaisson):
        os.makedirs(folderCaisson)
    if not os.path.exists(folderSeparation):
        os.makedirs(folderSeparation)
    if not os.path.exists(folderFissure):
        os.makedirs(folderFissure)
    if not os.path.exists(folderOthers):
        os.makedirs(folderOthers)
    #************************************************
    state =''
    for imagePath in glob.glob(path):
        i+=1
        imageName = imagePath.split("/")[-1] # take the latest element as name of the image
        gray = syrine.loadImage(imagePath)  #Load a single imge  
        #mean = int(gray.mean())    
        #print("mean = " ,str(mean))
        thresh = syrine.threshold(gray,"triangle")     # binarization of the loaded image
        # chose alpha and beta to adjust contrast of the img
        alpha = 3.0
        beta= 0
        contrast = syrine.contrast(gray, alpha, beta)
        #syrine.show('Contrast', contrast)
        # call processImage function
        img_with_colored_contours, state = syrine.processImage(gray, contrast, thresh)
        if state == CRACK :
            print(imageName)
            print(state)
            syrine.saveImage(folderFissure +"/"+ imageName, img_with_colored_contours) # save img in crack folder
        
        if state == SEPARATION :
            print(imageName)
            print(state)
            syrine.saveImage(folderSeparation +"/"+ imageName, img_with_colored_contours)

        if state == CAISSON :
            print(imageName)
            print(state)
            syrine.saveImage(folderCaisson +"/"+ imageName, img_with_colored_contours)

        if state ==OTHERS :
            print(imageName)
            print(state)
            syrine.saveImage(folderOthers +"/" +imageName, img_with_colored_contours)

    print("Done")