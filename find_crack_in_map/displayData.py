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
    