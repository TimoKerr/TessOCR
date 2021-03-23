import requests
import streamlit as st
import io
import base64

from requests_toolbelt.multipart.encoder import MultipartEncoder

# interact with FastAPI
backend = "http://127.0.0.1:8000/OCR"




def process(image, server_url: str):

    m = MultipartEncoder(fields={"file": ("filename", image, "image/jpeg")})

    r = requests.post(
        server_url, data=m, headers={"Content-Type": m.content_type}, timeout=8000
    )

    return r

def download_link(object_to_download, download_filename, download_link_text):
    """
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')
    """
    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'


st.title("OCR of Prakrit texts")
st.header("Inuits")
st.write("""This application will receive a non-editable document as input,
for example a pdf, png, or jpg, and return an editable text in .txt format.
For more information about the API go to http://127.0.0.1:8000/docs""")

input_image = st.file_uploader("Upload image")

if st.button("Let's GO(CR)!"):
    
    if input_image:
        text = process(input_image, backend)
        processed_text = text.content.decode("utf-8")
        st.write(processed_text)
        
        if st.button('Download as a text file'):
            tmp_download_link = download_link(processed_text, 'OCR_OUTPUT.txt', 'Click to download!')
            st.markdown(tmp_download_link, unsafe_allow_html=True)
        
        st.image(input_image)
    else:
        st.write("Please, insert image :}")

if st.button("Stop"):
    st.stop()
    pass

