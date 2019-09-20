import cv2
import numpy as np

smallRect = 10
crack = {'mean' : 10,'width_min': 9, 'width_max' : 60 ,'height_min': 100,'height_max' :500}
separation = {'mean' : 10, 'width_min': 4, 'width_max' : 30 ,'height_min': 100,'height_max' :900}
caisson = {'width_min': 60, 'width_max' : 250 ,'height_min': 600,'height_max' :1100}


SEPARATION = "SEPARATION"
CRACK = "CRACK"
CAISSON = "CAISSON"
NOISE = "NOISE"
OTHERS = "OTHERS"

BLUE = (255,0,0)
GREEN = (0,255,0)
RED = (0,0,255)
YELLOW = (255,255,0)

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


def get_contour_type(img,contour):
    rect = cv2.minAreaRect(contour)
    width = rect[1][0]
    height = rect[1][1]
    if width > smallRect and height > smallRect :
        cropImage = crop(img, rect)
        mean = cropImage.mean()
        
        ##################################################  fisssure  ######################################
        width = rect[1][0]
        height = rect[1][1]
        if ((mean > crack['mean']) and (width in range(crack['width_min'],crack['width_max'])) and (height in range(crack['height_min'],crack['height_max'])) ) :   
            print("crack detected")
            return CRACK, rect

        width = rect[1][1]
        height = rect[1][0]
        if ((mean > crack['mean']) and (width in range(crack['width_min'],crack['width_max'])) and (height in range(crack['height_min'],crack['height_max'])) ) :   
            print("crack detected")
            return CRACK, rect

        ##################################################  Separation  ######################################
        width = rect[1][0]
        height = rect[1][1]
        if ((mean < separation['mean']) and (width in range(separation['width_min'],separation['width_max'])) and (height in range(separation['height_min'],separation['height_max']))) :
            print("separation")
            return SEPARATION, rect

        width = rect[1][1]
        height = rect[1][0]
        if ((mean < separation['mean']) and (width in range(separation['width_min'],separation['width_max'])) and (height in range(separation['height_min'],separation['height_max']))) :
            print("separation")
            return SEPARATION, rect

        ##################################################  Caisson  ######################################
        width = rect[1][0]
        height = rect[1][1]
        if (width in range(caisson['width_min'],caisson['width_max'])) and (height in range(caisson['width_min'],caisson['width_max'])):
            print("caisson")
            return CAISSON, rect

        width = rect[1][1]
        height = rect[1][0]
        if (width in range(caisson['width_min'],caisson['width_max'])) and (height in range(caisson['width_min'],caisson['width_max'])):
            print("caisson")
            return CAISSON, rect
    print("others")
    return OTHERS, rect

def processImage(gray, contrast, thresh):
    img_with_colored_contours = contrast.copy()
    _,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # remove noise
    #contours = remove_noise(contours)
    #find the type to the image
    state = ''
    for contour in contours:
        state, rect = get_contour_type(gray,contour)
        if state == CRACK :
            color = BLUE
            folder = "crack/"
        elif state == SEPARATION: 
            color = GREEN
            folder = "separation/"
        elif state == CAISSON:
            color = RED
            folder = "caisson/"
        elif state == OTHERS :
            color = YELLOW
            folder = "others/"
                 
        box= cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(img_with_colored_contours,[box],0,color, 2)

    return img_with_colored_contours, state
