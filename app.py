from dotenv import load_dotenv
import streamlit as st
from pdf2image import convert_from_bytes
import os
import google.generativeai as genai
from PIL import Image

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,image,query=None):
    model = genai.GenerativeModel("gemini-pro-vision")
    if query is not None:
        response = model.generate_content([input,image,query])
    else:
        response = model.generate_content([input,image])

    return response.text

def input_resumedata(uploaded_file):
    if uploaded_file is not None:
        pdf_bytes = uploaded_file.read()
        images = convert_from_bytes(pdf_bytes, first_page=1, last_page=1)
        return images[0]
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="Resume Data Extractor")

st.header("Resume Data")

uploaded_file = st.file_uploader("Choose a file...", type=["pdf"])

image_data = None

if uploaded_file is not None:
    image_data = input_resumedata(uploaded_file)
    st.image(image_data, caption='Resume', use_column_width=True)
    query = st.text_input(label="What details you want from the resume?")
    query_button = st.button("Get Answer")

    submit = st.button("Extract all data")


    input_prompt = """
        You are a resume analyzer. You have to extract the data from the resume image. 
        You will have to answer the questions based on the input resume image.
    """


    if submit and image_data is not None:
        response = get_gemini_response(input_prompt,image_data)
        st.subheader("The response is:")
        st.write(response)

    if query_button and image_data is not None:
        response = get_gemini_response(input_prompt,image_data, query)
        st.subheader("The response is:")
        st.write(response)

