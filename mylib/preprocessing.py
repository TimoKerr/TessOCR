import cv2

def uniform_binarisation(img):
    """ uses uniform binarisation"""
    bin_img, image = cv2.threshold(img,140,255,cv2.THRESH_BINARY)
    return bin_img, image

def adaptive_binarisation(img):
    """ uses gausian binarisation with two params, block size and Constant
        First converts into grayscale because necessary. """
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    image = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,17,2)
    return image

def otsu_binarisation(img):
    """ uses otsu binarisation (Good for BIMODAL & after Gaussia filter) """
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur_img = cv2.GaussianBlur(img_gray,(1,1),0)
    bin_img,image = cv2.threshold(blur_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return bin_img, image
    

def super_res(img, scale):
    """ Rescales and superres """
    bicubic = cv2.resize(img, (img.shape[1]*scale, img.shape[0]*scale),
    interpolation=cv2.INTER_CUBIC)
    return bicubic


def denoise(img):
    """ Noise removal """
    dn_img = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
    return dn_img


def erosion(img):
    """ Thinning and rerosion to find skeleton """
    kernel = np.ones((2,2),np.uint8)
    erosion_img = cv2.erode(img,kernel,iterations = 1)
    return erosion_img


def pipeline(img, scale):
    img = denoise(img)
    img = super_res(img, scale)
    img_bn, img = otsu_binarisation(img)
    return img

def define_boundaries(img):
    """ Function that detects the contours and removes all the noise that is not text.
    Finds contours, keeps track of the largest one, draws contours on image"""
    ret, th = cv2.threshold(img, 127,255, 0)    
    contours, hierarchy = cv2.findContours(th, cv2.RETR_EXTERNAL, 1)
    cnts = contours
    max = 0    #----Variable to keep track of the largest area----
    c = 0      #----Variable to store the contour having largest area---
    for i in range(len(contours)):
        if (cv2.contourArea(cnts[i]) > max):
            max = cv2.contourArea(cnts[i])
            c = i
    rgb_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    #rep = cv2.drawContours(rgb_img, contours, c, (0,255,0), 3) 

    mask = np.zeros_like(img_processed_lic) # Create mask where white is what we want, black otherwise
    cv2.drawContours(mask, contours, c, 255, -1) # Draw filled contour in mask
    out = np.zeros_like(img_processed_lic) # Extract out the object and place into output image
    out[mask == 255] = img_processed_lic[mask == 255]

    return out