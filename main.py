import cv2
import pytesseract
import io

from pytesseract import Output
from PIL import Image
from fastapi.responses import FileResponse
from fastapi import FastAPI, File, UploadFile

from mylib import preprocessing


app = FastAPI()
result_path = "output.txt"


@app.get("/")
def read_root():
    return {"App use": "OCR-engine"}


@app.post("/OCR/")
async def create_file(file: bytes = File(...)):
    input_image = Image.open(io.BytesIO(file)).convert("RGB")
    text = pytesseract.image_to_string(input_image, lang="hin+eng", config="--psm 3")
    text = text.replace("\n", "  \n")
    #text = text.replace("\f", " ")
    with open("output.txt", "w") as output_file:
        output_file.write(text)

    return text


@app.get("/result/")
async def result():
    return FileResponse(path=result_path, filename="output.txt", media_type="text")
