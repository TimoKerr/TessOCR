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