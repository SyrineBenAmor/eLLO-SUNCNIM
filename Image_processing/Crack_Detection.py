import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import time
import os

import syrineLib as syrine

global path

path = "gather_Data/photos/"+time.strftime("%d-%m-%Y")+"/"+"*.jpg"
#**********************************************************


def detectcrack():#replace with def deteccrack(path):
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
    
    for imagePath in glob.glob(path):
        i+=1
        imageName = imagePath.split("/")[-1] # take the latest element as name of the image
        gray = syrine.loadImage(imagePath)  #Load a single imge  
        mean = int(gray.mean())    
        #print("mean = " ,str(mean))
        thresh = syrine.threshold(gray,"triangle")     # binarization of the loaded image
        alpha = 3.0
        beta= 0
        contrast = syrine.contrast(gray, alpha, beta)
        #syrine.show('Contrast', contrast)
        outContrast,state = syrine.processImage(gray, contrast, thresh)
        if state == "separation" :
            thresh = syrine.threshold(gray,"binary")
            outContrastBis,state = syrine.processImage(gray, contrast, thresh)
            if state != "caisson" : #it's a separation image
                #syrine.show('rectangle '+str(i),outContrast)
                syrine.saveImage(folderSeparation +"/" + imageName,outContrast)
            else :#it's caisson image
                #syrine.show('rectangle '+str(i),outContrastBis) 
                syrine.saveImage(folderCaisson +"/" + imageName,outContrastBis)
        elif state == 'fissure' :#fissure
            #syrine.show('rectangle '+str(i),outContrast)
            syrine.saveImage(folderFissure +"/" + imageName,outContrast)
        elif state == 'caisson' : #caisson
            syrine.saveImage(folderCaisson +"/" + imageName,outContrast)
        else: #black image (without contours)
            syrine.saveImage(folderOthers +"/" + imageName,outContrast) 
    print("Done")