from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st

from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Gemini-Pro-Vision
model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input, image, prompt):
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,    # Get the mime type of the uploaded file.
                "data": bytes_data                 # Get the bytes of the uploaded file.
            }]
        return image_parts
    else:
        raise FileNotFoundError("No file has been uploaded")


st.set_page_config(page_title="Multi Language Invoice Information Extractor")
st.header("Multi Language Invoice Information Extractor")
input = st.text_input("Inpute Prompt: ", key='input')
uploaded_file = st.file_uploader("Upload Image of the invoice: ", type=["jpg", "jpeg", "png"])
image=""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

submit = st.button("Tell me about the invoice")

input_prompt = """ 
You are an expert in understanding invoices. We will upload an image 
as an invoice and you will have to answer any question based on the uploaded invoice image.
"""

# If submit button is clicked
# First need to get image data
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input, image_data, input_prompt)
    st.subheader("The response is : ")
    st.write(response)


