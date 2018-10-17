import glob
import time

class fetchData():
    def __init__(self,pathImage,pathDatafile):
        self.pathImage = pathImage
        self.pathDatafile = pathDatafile
        self.timeImageArray = self.timeImage()
        self.gpsDataArray = self.timeData()

        def timeImage(self):
        timeImageArray =[]
        for imagePath in glob.glob(self.pathImage):
            time_Image = imagePath.split("/")[-1]
            time_Image = time_Image.split(".")[0]
            timeImageArray.append(time_Image)
        return timeImageArray
        
    def timeData(self):
        gpsDataArray = []
        dataFile = open(self.pathDatafile,'r')
        for line in dataFile:
            time_data = line.split(",")[0]
            for i in range(0,len(self.timeImageArray)):
                if time_data == self.timeImageArray[i]:
                    gpsData =line.split(",")[-1]
                    gpsDataArray.append(gpsData)
                else : 
                    i=i+1            
        dataFile.close()
        return(gpsDataArray)
    