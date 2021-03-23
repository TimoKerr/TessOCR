import cv2
import pytesseract
from pytesseract import Output
from PIL import Image
import io


from fastapi import FastAPI, File, UploadFile

from mylib import preprocessing

app = FastAPI()

@app.get("/")
def read_root():
    return {"App use": "OCR-engine"}

@app.post("/OCR/")
async def create_file(file: bytes = File(...)):
    input_image = Image.open(io.BytesIO(file)).convert("RGB")
    text = pytesseract.image_to_string(input_image,lang='hin+eng',config ='--oem 3')
    text = text.replace("\n", " ")
    with open("output.txt", "w") as output_file:
        output_file.write(text)
    return text, output_file



