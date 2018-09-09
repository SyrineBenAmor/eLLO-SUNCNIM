import numpy as np
import cv2
mirorRect = {'width' : 14, 'height' : 86}
heightSite = 18.55 # largeur site =  18,55 m
widthSite = 53.35 # longeur site = 53,348 m


class pinMap():
    def __init__(self, sitePlanPath):
        self.image = cv2.imread(sitePlanPath)
        self.imageFilter = self.filter()
        
        

    def brokenMirrors(self,realCoordinate):

        self.realCoordinate = realCoordinate
        self.Caissons = self.listOfCaisson()
        self.newOrigin = self.origin()
        self.coordinateInPixel = self.convertRealCoordinateToPixel()
        self.ancientCoordinate = self.ancientPointCoordinate()
        self.nearestCaisson = self.findCaisson()
        self.image = self.colorCaisson()
       
        return self.image
        
    def filter(self):

        plan = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        rows, cols = plan.shape[:2]
        print("Image Dimensions : " +str([rows, cols]))
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
        
        return masked_image

    
    def listOfCaisson (self):

        _,contours,_ = cv2.findContours(self.imageFilter, 1, 2)
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
        print("rect =",rect)
        newOrigin = (int(rect[0][0]-rect[1][0]/2),int(rect[0][1]+rect[1][1]/2))
        return newOrigin

    def convertRealCoordinateToPixel(self):
        x = 61
        y = 579
        coordinatepointOrig = (x, y) 
        coordinatepoint1 = (769, y)
        coordinatepoint2 = (x,335)

        coordinateInPixelX = (self.realCoordinate[0]*(coordinatepoint1[0]-x))/widthSite
        coordinateInPixelY = (self.realCoordinate[1]*(y-coordinatepoint2[1]))/heightSite
        coordinateInPixel = (coordinateInPixelX,coordinateInPixelY)
        return coordinateInPixel

    def ancientPointCoordinate(self):

        ancientCoordinatePointX= self.coordinateInPixel[0]+self.newOrigin[0]
        ancientCoordinatePointY= self.coordinateInPixel[1]+self.newOrigin[1]
        ancientCoordinate = (ancientCoordinatePointX,ancientCoordinatePointY)
        return ancientCoordinate

    def findCaisson(self):
        
        ShortestDistanceToCaisson = -1000
        nearestCaisson = 0
        for caisson in self.Caissons:
            distance = cv2.pointPolygonTest(caisson,self.ancientCoordinate,True)             #it returns +distance if the point is inside the contour
                                                                                 #it returns -distance if the point is outside the contour
                                                                                #it returns 0 if the point is on the contour  
            if  (distance >= 0) :
                print("point is inside the contour",caisson)
                nearestCaisson = caisson
                return nearestCaisson
            else:
                if (abs(distance) < abs(ShortestDistanceToCaisson)):
                    ShortestDistanceToCaisson = distance
                    nearestCaisson = caisson
                    print("point is near to the contour",nearestCaisson)
        return nearestCaisson


    
    def colorCaisson(self):

        
        cv2.drawContours(self.image,[self.nearestCaisson], 0,(0,0,255),-1) # for filling inside a specific contour
        
        return self.image
