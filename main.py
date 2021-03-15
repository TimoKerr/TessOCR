import cv2
import pytesseract
import pandas

from mylib import preprocessing

image_name = "data/prakrit_2.png"
img_cv2 = cv2.imread(image_name)
print(img_cv2.dtype)

img_preprocessed = preprocessing.pipeline(img_cv2, 3)

cv2.imwrite("data/Preprocessed_image.png", img_preprocessed)

text = pytesseract.image_to_string(img_preprocessed,lang='hin+eng')
with open('output/OCRd.txt', mode = 'w') as f:
    f.write(text)
