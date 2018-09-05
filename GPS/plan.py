import numpy as np
import cv2
mirorRect = {'width' : 14, 'height' : 86}
heightSite = 18.55 # largeur site =  18,55 m
widthSite = 53.348 # longeur site = 53,348 m


def filter(planSite):

    plan_orig = cv2.imread(planSite)
    plan = cv2.cvtColor(plan_orig, cv2.COLOR_BGR2GRAY)
    rows, cols = plan.shape[:2]
    print("Image Dimensions : " +str([rows, cols]))
    mean=plan.mean()
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


def listOfCaisson (Masked_image):

    _,contours,_ = cv2.findContours(Masked_image, 1, 2)
    caissons = []
    # Find all caisson
    for contour in contours :
        rect = cv2.minAreaRect(contour)
        if (1<rect[1][0] < mirorRect['width']) and (0 < rect[1][1] < mirorRect['height']) :
            caissons.append(contour)
    return caissons

def origin(image):
    _,contours,_ = cv2.findContours(image, 1, 2)
    rect = cv2.minAreaRect(contours[7])
    widthcaisson = 84
    heightcaisson = 12
    newOrigin = (int(rect[0][0]-widthcaisson/2),int(rect[0][1]+heightcaisson/2))
    return newOrigin



def findCaisson(pointCoordinate,listOfCaisson):
    
    ShortestDistanceToCaisson = -1000
    nearestCaisson = 0
    for caisson in listOfCaisson:
        distance = cv2.pointPolygonTest(caisson,pointCoordinate,True)             #it returns +distance if the point is inside the contour
                                                                             #it returns -distance if the point is outside the contour
                                                                            #it returns 0 if the point is on the contour  
        if  (distance >= 0) :
            print("point is inside the contour",caisson)
            return caisson
        else:
            if (abs(distance) < abs(ShortestDistanceToCaisson)):
                ShortestDistanceToCaisson = distance
                nearestCaisson = caisson
                print("point is near to the contour",nearestCaisson)
    return nearestCaisson


def colorCaisson(image, caisson):

    image = cv2.imread(image)
    cv2.drawContours(image,[caisson], 0,(0,0,255),-1) # for filling inside a specific contour
    
    return image

def convertRealCoordinateToPixel(image,realCoordinate):
    x=61
    y= 579
    coordinatepointOrig = (x,y) 
    coordinatepoint1 = (769,y)
    coordinatepoint2 = (x,335)

    image = cv2.imread(image)
    cv2.line(image,coordinatepointOrig,coordinatepoint1,(255,0,0),1)

    coordinateInPixelX = (realCoordinate[0]*(coordinatepoint1[0]-x))/widthSite
    coordinateInPixelY = (realCoordinate[1]*(y-coordinatepoint2[1]))/heightSite
    coordinateInpixel = (coordinateInPixelX,coordinateInPixelY)
    return image, coordinateInpixel

    