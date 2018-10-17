import numpy as np
import cv2
import math


mirorRect = {'width' : 14, 'height' : 86}
heightSiteInMeters = 18.55 # largeur site =  18,55 m
widthSiteInMeters = 53.35 # longeur site = 53,348 m
LatOrigin = 43.11653833333333 #latitude of the initial position of the robot in the prototype site
LonOrigin = 5.882466666666666 #longitude of the initial position of the robot in the prototype site

class pinMap():
    def __init__(self, sitePlanPath):
        self.image = cv2.imread(sitePlanPath)
        self.imageFilter = self.Filter(self.image)
        self.newOrigin = self.origin()     
        
    def brokenMirrors(self,gpsCoordinate):      
        realCoordinate = self.convertLatitudeLongitudeToMeters(gpsCoordinate)
        coordinateInPixel = self.convertRealCoordinateToPixel(realCoordinate)
        ancientCoordinate = self.ancientPointCoordinate(coordinateInPixel)
        nearestCaisson = self.findCaisson(self.imageFilter,ancientCoordinate)
        self.image = self.colorCaisson(self.image,nearestCaisson)
        
        return self.image
        
    def Filter(self, image):

        plan = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rows, cols = plan.shape[:2]
        #print("Image Dimensions : " +str([rows, cols]))
        mean = plan.mean()
        _,thresh = cv2.threshold(plan, mean-50, 255,  cv2.THRESH_BINARY)
        

        # fix polygon vertex
        top_left    = [0, rows*0.35]
        top_right   = [cols, rows*0.35]
        bottom_left = [0, rows*0.65]
        bottom_right= [cols, rows*0.65]

        vertices = np.array([[bottom_left,top_left, top_right, bottom_right]], dtype=np.int32)

        #apply mask to the thresh image
        mask = np.zeros_like(thresh)                                    #initialize a black mask
        cv2.fillPoly(mask, vertices, 255)                               # fill the inside of polygon with white 
        masked_image = cv2.bitwise_and(thresh, mask)                    # apply the mask to the binary image
        cv2.imshow("masked image",masked_image)
        return masked_image

    
    def listOfCaisson (self, image):

        _,contours,_ = cv2.findContours(image, 1, 2)
        Caissons = []
        # Find all caisson
        for contour in contours :
            rect = cv2.minAreaRect(contour)
            if (1<rect[1][0] < mirorRect['width']) and (0 < rect[1][1] < mirorRect['height']) :
                Caissons.append(contour)
        return Caissons
    
    def origin(self):
        _,contours,_ = cv2.findContours(self.imageFilter, 1, 2)
        rect = cv2.minAreaRect(contours[7])
        newOrigin = (int(rect[0][0] - rect[1][1]/2),int(rect[0][1] + rect[1][0]/2))
        return newOrigin

    def convertRealCoordinateToPixel(self, realCoordinate):
       
        coordinatepoint1 = (769, self.newOrigin[1])
        coordinatepoint2 = (self.newOrigin[0],335)
        siteWidthInPixels = (coordinatepoint1[0]-self.newOrigin[0])
        siteHeightInPixels = (self.newOrigin[1]-coordinatepoint2[1])

        coordinateInPixelX = (realCoordinate[0]*siteWidthInPixels)/widthSiteInMeters
        coordinateInPixelY = (realCoordinate[1]*siteHeightInPixels)/heightSiteInMeters
        
        return int(coordinateInPixelX),int(coordinateInPixelY)
        

    def ancientPointCoordinate(self, coordinateInPixel ):

        ancientCoordinatePointX = coordinateInPixel[0] + self.newOrigin[0]
        ancientCoordinatePointY = -coordinateInPixel[1] + self.newOrigin[1]
        return ancientCoordinatePointX,ancientCoordinatePointY


    def findCaisson(self, image, coordinate):
        
        ShortestDistanceToCaisson = -1000
        nearestCaisson = 0
        Caissons = self.listOfCaisson(image)
        
        for caisson in Caissons:
            distance = cv2.pointPolygonTest(caisson, coordinate,True)             #it returns +distance if the point is inside the contour
                                                                                 #it returns -distance if the point is outside the contour
                                                                                #it returns 0 if the point is on the contour  
            if  (distance >= 0) :
                #print("point is inside the contour",caisson)
                nearestCaisson = caisson
                return nearestCaisson
            else:
                if (abs(distance) < abs(ShortestDistanceToCaisson)):
                    ShortestDistanceToCaisson = distance
                    nearestCaisson = caisson
        #print("point is near to the contour",nearestCaisson)
        return nearestCaisson


    
    def colorCaisson(self, image,nearestCaisson):

        
        cv2.drawContours(image,[nearestCaisson], 0,(0,0,255),-1) # for filling inside a specific contour
        
        return image

    def convertLatitudeLongitudeToMeters(self,gpsCoordinate):
        R = 6372  #approximate radius of earth in Km
        lat = 43.11655333333333
        lon = 5.882485000000001

        
        dlon = math.radians(lon - LonOrigin)
        dlat = math.radians(lat - LatOrigin)

        a = math.sin(dlat /2)**2 + math.cos(math.radians(LatOrigin)) * math.cos(math.radians(lat)) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))

        distance = R * c #distance en Km
        print("distance [m] = ",distance*1000)

        dy = (lon-LonOrigin)* 40000*math.cos((LatOrigin+lat)*math.pi/360)/360
        dx = (LatOrigin - lat)*40000/360
        print("x [m], y [m]=" ,abs(dx*1000), abs(dy*1000))
        realCoordinate = abs(dx*1000),abs(dy*1000)
        return realCoordinate

        
        
        
