import cv2
import numpy as np

#fix dimensions of contours that we want to detect in an image
smallRect = 10 #dimensions of noise contour
crack = {'mean' : 10,'width_min': 9, 'width_max' : 200 ,'height_min': 100,'height_max' :550}
separation = {'mean' : 10 , 'width_min': 4, 'width_max' : 40 ,'height_min': 100,'height_max' :1000}
caisson = {'width' : 100 ,'height': 600}

# Declaration 
SEPARATION = "SEPARATION"
CRACK = "CRACK"
CAISSON = "CAISSON"
NOISE = "NOISE"
OTHERS = "OTHERS"

#different color for different contours type
BLUE = (255,0,0) # blue for crack contours
GREEN = (0,255,0) # green for separation contours
RED = (0,0,255) # red for caisson contours
YELLOW = (0,255,255) # yellow for the rest of contours


####################### Cut the part you want to treat from an image #######################################
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
######################### adjust contrast ##############################################
def contrast(img, alpha, beta) :
    mul = cv2.multiply(img,np.array([alpha]))
    contrast = cv2.add(mul,beta)
    contrast = cv2.cvtColor(contrast, cv2.COLOR_GRAY2BGR) 
    return contrast
######################### load image ##############################################
def loadImage(imagePath):
    img = cv2.imread(imagePath) # load image from directory
    img = cv2.resize(img, None, fx=0.4 , fy=0.4, interpolation=cv2.INTER_CUBIC) # resize the image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert colored image to gray image
    img = cv2.medianBlur(img,3) #apply median filter
    return img
######################### Thresholding ##############################################
def threshold(img, threshType):
    if threshType == "triangle" :
        _,thresh = cv2.threshold(img, 1, 255,  cv2.THRESH_TRIANGLE)
    elif threshType == "binary" :
        _,thresh = cv2.threshold(img, 1, 255,  cv2.THRESH_BINARY)
    return thresh
######################### show and save image ##############################################
def show(label, img):
    cv2.imshow(label, img)
def saveImage(path,img):
    cv2.imwrite(path,img)

######################### get contour type ##############################################
def get_contour_type(img,contour):
    rect = cv2.minAreaRect(contour) # find a rotated rectangle of the minimum area
    width = rect[1][0] 
    height = rect[1][1]
    

    if width > smallRect and height > smallRect : #eliminate noise
        cropImage = crop(img, rect) # cut rectangle
        mean = cropImage.mean() # calcul the mean of pixels of the croped img
        #print ("rect  =", rect)
        #print ("mean= ", mean)
        ##################################################  fisssure  ######################################
        width = rect[1][0]
        height = rect[1][1]
        
        if (mean > crack['mean']) and (crack['width_min']<width <crack['width_max']) and (crack['height_min']<height <crack['height_max']) :   
            #print("crack detected")
            return CRACK, rect
        #reverse width and hight value
        width = rect[1][1]
        height = rect[1][0]
        
        if (mean > crack['mean']) and (crack['width_min']<width <crack['width_max']) and (crack['height_min']<height <crack['height_max']) :   
            #print("crack detected")
            return CRACK, rect

        ##################################################  Separation  ######################################
        width = rect[1][0]
        height = rect[1][1]
        if ((mean < separation['mean']) and (width in range(separation['width_min'],separation['width_max'])) and (height in range(separation['height_min'],separation['height_max']))) :
            #print("separation")
            return SEPARATION, rect

        width = rect[1][1]
        height = rect[1][0]
        if ((mean < separation['mean']) and (width in range(separation['width_min'],separation['width_max'])) and (height in range(separation['height_min'],separation['height_max']))) :
            #print("separation")
            return SEPARATION, rect

        ##################################################  Caisson  ######################################
        width = rect[1][0]
        height = rect[1][1]
        if width > caisson['width'] and height > caisson['height']:
            #print("caisson")
            return CAISSON, rect

        width = rect[1][1]
        height = rect[1][0]
        if width >  caisson['width'] and height > caisson['height']:
            #print("caisson")
            return CAISSON, rect
    #print("others")
    return OTHERS, rect
################################### treat image ############################################################
def processImage(gray, contrast, thresh):
    img_with_colored_contours = contrast.copy() #copy the image after adjusting contrast
    _,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #find all contours in the img

    #find the type of the image
    state = ''
    states =[] 
    for contour in contours:
        state, rect = get_contour_type(gray,contour)
        if state == CRACK :
            color = BLUE
            states.append(state) #add the state in the list states
        elif state == SEPARATION: 
            color = GREEN
            states.append(state)
        elif state == CAISSON:
            color = RED
            states.append(state)
        elif state == OTHERS :
            color = YELLOW
            states.append(state)    
        box= cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(img_with_colored_contours,[box],0,color, 2) # draw contours

    if CRACK in states : # if the state crack in the states list save the image take the state crack
        state = CRACK
    if CRACK not in states: #
        if SEPARATION in states:
            state = SEPARATION
            
        if SEPARATION not in states:
            if  CAISSON in states:
                state = CAISSON
            
            if CAISSON not in states:
                state = OTHERS
            
    return img_with_colored_contours, state
