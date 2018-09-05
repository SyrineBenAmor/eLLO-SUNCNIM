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
    newOrigin = rect[0]
    return newOrigin



def statePoint(coordinatePoint,listOfContours):
    
    ShortestDistance = -50000
    shortestContour = 0
    for contour in listOfContours: 

        distance = cv2.pointPolygonTest(contour,coordinatePoint,True)             #it returns +distance if the point is inside the contour
                                                                             #it returns -distance if the point is outside the contour
                                                                            #it returns 0 if the point is on the contour  
        if  (distance >= 0) :
            print("point is inside the contour",contour)
            return contour
            
        else:
            if (abs(distance) < abs(ShortestDistance)):
                ShortestDistance = distance
                shortestContour = contour
                
    return shortestContour


def changeColorInsideContour(image,contour):

    image = cv2.imread(image)
    cv2.drawContours(image,[contour], 0,(0,0,255),-1) # for filling inside a specific contour
    return image