import requests
import streamlit as st
import io
import os

from requests_toolbelt.multipart.encoder import MultipartEncoder

# interact with FastAPI
backend = "http://127.0.0.1:8000/OCR/"
download_link = "http://127.0.0.1:8000/result/"


def process(image, server_url: str):

    m = MultipartEncoder(fields={"file": ("filename", image, "image/jpeg")})

    r = requests.post(
        server_url, data=m, headers={"Content-Type": m.content_type}, timeout=8000
    )

    return r


st.title("OCR of Prakrit texts")
st.header("Inuits")
st.write(
    """This application will receive a non-editable document as input,
for example a pdf, png, or jpg, and return an editable text in .txt format.
For more information about the API go to http://127.0.0.1:8000/docs"""
)

input_image = st.file_uploader("Upload image")

if st.button("Let's GO(CR)!"):

    if input_image:
        text = process(input_image, backend)
        processed_text = text.content.decode("utf-8")
        st.header("Output")
        st.markdown(processed_text)
        st.header("Original Image")
        st.image(input_image)
        st.markdown("Download output: " + download_link)

    else:
        st.write("Please, insert image :}")
