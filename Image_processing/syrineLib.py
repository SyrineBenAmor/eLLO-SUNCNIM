import cv2
import numpy as np

smallRect = 10
bigRect = {'width' : 150, 'height' : 100}
separation = {'width' : 150, 'height' : 60}
crack = {'mean' : 12, 'width' : 200}

def crop(img, rect):

    # rotate img
    angle =   rect[2]
    rows,cols = img.shape[0], img.shape[1]
    M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
    img_rot = cv2.warpAffine(img,M,(cols,rows))

    # rotate bounding box
    rect0 = (rect[0], rect[1], 0.0)
    box = cv2.boxPoints(rect)
    pts = np.int0(cv2.transform(np.array([box]), M))[0]    
    pts[pts < 0] = 0
    # crop
    crop = img_rot[pts[1][1]:pts[0][1], 
                       pts[1][0]:pts[2][0]]
    return crop

def contrast(img, alpha, beta) :
    mul = cv2.multiply(img,np.array([alpha]))
    contrast = cv2.add(mul,beta)
    contrast = cv2.cvtColor(contrast, cv2.COLOR_GRAY2BGR) 
    return contrast

def loadImage(imagePath):
    img = cv2.imread(imagePath)
    img = cv2.resize(img, None, fx=0.4 , fy=0.4, interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.medianBlur(img,3)
    return img

def threshold(img, threshType):
    if threshType == "triangle" :
        _,thresh = cv2.threshold(img, 1, 255,  cv2.THRESH_TRIANGLE)
    elif threshType == "binary" :
        _,thresh = cv2.threshold(img, 1, 255,  cv2.THRESH_BINARY)
    return thresh

def show(label, img):
    cv2.imshow(label, img)
def saveImage(path,img):
    cv2.imwrite(path,img)

def processImage(gray, contrast, thresh):
    outContrast = contrast.copy()
    state = ''
    _,contours,_ = cv2.findContours(thresh,1,2)
    nbContoursFound = len(contours)
    #print("contours found "+str(nbContoursFound))
    nbContoursSelected = 0
    biggestRect = 0
    brightRect = 0
    rects = []
    for cnt in contours :
        rect = cv2.minAreaRect(cnt)
        #rect = cv2.boundingRect(cnt)
        if rect[1][0] > bigRect['width'] and rect[1][1] > bigRect['height'] : # look for a big Rect
            if biggestRect == 0 :
                biggestRect = rect
            else :
                if (rect[1][0]*rect[1][1]) > (biggestRect[1][0]*biggestRect[1][1]):
                    biggestRect = rect
        else : #biggest Rect is not added to the List (minimize time)
            if rect[1][0] > smallRect and rect[1][1] > smallRect : #eliminate small rects
                cropImage = crop(gray, rect)
                mean = cropImage.mean()
                if  mean > crack['mean'] and rect[1][0] > crack['width']:
                    brightRect = rect
                rects.append(rect) # add rect to list of rects
    
    if biggestRect != 0 :
        box= cv2.boxPoints(biggestRect)
        box = np.int0(box)
        cv2.drawContours(outContrast,[box],0,(0,0,255),2)
        print("Caisson")
        state = "caisson"
    else :
        for rect in rects :
            #print(rect)
            if (rect[1][0] > separation['width'] and rect[1][1] < separation['height'] ) or (rect[1][0] < separation['height'] and rect[1][1] > separation['width']):
                box= cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.drawContours(outContrast,[box],0,(0,255,0),2)
                x,y = box[2][0],box[2][1]
                print("Separation")
                state = "separation"
    if brightRect != 0 :
        box= cv2.boxPoints(brightRect)
        box = np.int0(box)
        cv2.drawContours(outContrast,[box],0,(255,0,0),2)
        print("Crack Detected , better Call Adrien 0611223344")
        state = "fissure"
    return outContrast, state


