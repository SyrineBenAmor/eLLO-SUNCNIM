import numpy as np
import cv2
mirorRect = {'width' : 14, 'height' : 86}
heightMirror = 100 # largeur miroir = 100 cm
widthMirror = 160 # longeur miroir = 160 cm


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
    
    return (masked_image)

def listOfContours (Masked_image):

    _,contours,_ = cv2.findContours(Masked_image, 1, 2)
    listOfContours = []
    # Find all caisson
    for contour in contours :
        rect = cv2.minAreaRect(contour)
        if (1<rect[1][0] < mirorRect['width']) and (0 < rect[1][1] < mirorRect['height']) :
            listOfContours.append(contour)
    return listOfContours

def origin(image):
    _,contours,_ = cv2.findContours(image, 1, 2)
    rect = cv2.minAreaRect(contours[7])
    newOrigin = rect[0]
    return newOrigin



def statePoint(coordinatePoint,listOfContours):
    listOfDistance = []
    ShortestDistance = -500
    for contour in listOfContours: 

        distance = cv2.pointPolygonTest(contour,coordinatePoint,True)             #it returns +distance if the point is inside the contour
        listOfDistance.append(distance)                                     #it returns -distance if the point is outside the contour
                                                                            #it returns 0 if the point is on the contour  
        rect = cv2.minAreaRect(cnt)
        
        if 1<rect[1][0] < mirorRect['width'] and 0 < rect[1][1] < mirorRect['height'] :
            box= cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(plan_orig,[box],0,(255,0,0),2)
            rectOfAllMiror.append(rect)
                    
    return (plan_orig, rectOfAllMiror)
'''
def convertCoordinateToPixels(coordinateX , coordinateY, rect):

    rect = cv2.minAreaRect(contours[7])
    NeworiginPointRepairX = rect[0][0]
    NeworiginPointRepairY = rect[0][1]
    
    coordinatePixelH = (rect[1][0] * coordinateX )/heightMiror
    coordinatePixelW = (rect[1][1] * coordinateY) /widthMiror
    
    return (coordinatePixelH,coordinatePixelW )

x,y = convertCoordinateToPixels(10,100)
print(x,y)
            #get the first rect coordinate point to fix new origin repair
        
    print(NeworiginPointRepairX,NeworiginPointRepairY)   
'''    

def changeColorInsideContour(image,Contour):
    
    image = cv2.imread(image)
    cv2.drawContours(image,[Contour],0,(0,0,255),-1) # for filling inside a specific contour

    return image
        