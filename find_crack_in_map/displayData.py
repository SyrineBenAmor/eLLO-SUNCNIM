import glob
import time
import os

class fetchData(): # class that take 2 paths (dataFile.txt and folder of image (fissure folder)) and return all the coordinate of the gps
    def __init__(self,pathImage,pathDatafile):
        self.pathImage = pathImage
        self.pathDatafile = pathDatafile
        self.timeImageArray = self.timeImage()
        self.gpsDataArray = self.timeData()

    def timeImage(self): # stock name of image in the folder (fissure) in the array "timeImageArray" because name of the image is the same time of the data
        timeImageArray =[] # declare an empty array
        for imagePath in glob.glob(self.pathImage): # go through all the images existing in pathImage
            time_Image = imagePath.split("/")[-1] # imagePath :(Image_processing/image_processing_output/17-10-2018/fissure/10:10:01.jpg) so take the latest member wich is (10:10:01.jpg)
            time_Image = time_Image.split(".")[0] # split this member (10:10:01.jpg) and take the first one
            timeImageArray.append(time_Image) # stock time in "timeImageArray" 
        return timeImageArray
    
    def timeData(self): #Stock longitude and latitude from data file.txt in the array "gpsDataArray"
        gpsDataArray = [] #declare an empty array
        dataFile = open(self.pathDatafile,'r') # open file.txt for reading
        for line in dataFile: # go through every line in the file.txt
            time_data = line.split(",")[0] # split line and take the first member (which is time)
            for i in range(0,len(self.timeImageArray)): 
                if time_data == self.timeImageArray[i]: # for every time in "timeImageArray" verify if it's equal to the time line in the data file.txt
                    gpsData =line.split(",")[-1] #if they are equal split line and take the latest member (which is gps longitude and latitud)
                    gpsDataArray.append(gpsData) # stock latitude & longitude in the  "gpsDataArray" 
                else :
                    i=i+1      #increment counter i     
        dataFile.close() # close the data file
        return(gpsDataArray)
    
    def gpsDataCouple(self): # create a couple of latitude & longitude 
        CoordinateGPS =[] 
        for i in range(0,len(self.gpsDataArray)): # go through all the member in "gpsDataArray" (list = ['43.111;5.889 \n'])
            self.gpsDataArray[i] = self.gpsDataArray[i].split(";") #separate latitude & longitude (list = ['43.111' , '5.889 \n']
            coordinateXgps = self.gpsDataArray[i][0] # the x coordinate is the latitude  (first member)
            self.gpsDataArray[i][1]= self.gpsDataArray[i][1].split(" ") #separate the 2 members (list = ['5.889','\n'])
            coordinateYgps = self.gpsDataArray[i][1][0] # the y coordinate in the longitude (first member)
            CoordinateGPS.append(tuple((coordinateXgps,coordinateYgps))) # stock laltitud and longitude as a couple
        return CoordinateGPS