import cv2
import pytesseract

from fastapi import FastAPI, File, UploadFile

from mylib import preprocessing

image_name = "data/prakrit.png"
img_cv2 = cv2.imread(image_name)

img_preprocessed = preprocessing.pipeline(img_cv2, 3)
img_preprocessed_masked = preprocessing.define_boundaries(img_preprocessed)

cv2.imwrite("data/Preprocessed_image.png", img_preprocessed)
cv2.imwrite("data/Preprocessed_image_mask.png", img_preprocessed_masked)

text = pytesseract.image_to_string(img_preprocessed,lang='hin+eng')
with open('output/OCRd.txt', mode = 'w') as f:
    f.write(text)


app = FastAPI()


@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

