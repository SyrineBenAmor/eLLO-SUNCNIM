import glob
import time

class fetchData():
    def __init__(self,pathImage,pathDatafile):
        self.pathImage = pathImage
        self.pathDatafile = pathDatafile
        self.timeImageArray = self.timeImage()
        self.gpsDataArray = self.timeData()

    