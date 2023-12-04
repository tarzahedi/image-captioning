import streamlit as st
# import pandas as pd
# from io import StringIO
from PIL import Image
import requests
#import time
from gtts import gTTS
from io import BytesIO
#from image_interface.interface.main import open_image,preprocess,generate_caption
# from fastapi import FastAPI, File, UploadFile
# from typing import Annotated
# from image_interface.api.fast import predict_caption, predict_upload
#from elevenlabs import generate, play
#from pydantic import BaseModel, ConfigDict


base_url = "http://127.0.0.1:8000/"
# Streamlit app title
st.title("Image Captioning")

# Streamlit app content
st.header("Lets caption some pictures!")
#st.write("This is :blue[test]")

# Add a sidebar to the app
with st.sidebar:
    # Choice selector for the user in the sidebar
    st.markdown("<p style='font-size:20px; font-family:sans-serif; font-weight: bold;'>Choose an option:</p>", unsafe_allow_html=True)
    choice = st.radio("", ("Upload Image", "Provide URL", "Take a New Image"))


if choice == "Provide URL":

# # URL:
    input_url = st.text_input('Upload image via url:')

    if input_url is not None:
            # image = Image.open(requests.get(input_url, stream=True).raw).convert("RGB")
            # st.image(image)
        params = {"url": input_url}
        api_endpoint = f"{base_url}predict_url"

               # Use st.spinner to indicate progress
        #with st.spinner('Processing image...'):
        response = requests.get(api_endpoint, params=params)
            #time.sleep (4)

        if response.status_code == 200:
            caption = response.json()
            st.markdown("<p style='font-size:25px; font-family:sans-serif;'>Caption: {}</p>".format(response.json()), unsafe_allow_html=True)
# Text-to-speech - reading out the caption
            sound_file = BytesIO()
            tts = gTTS(caption, lang='en')
            tts.write_to_fp(sound_file)
            st.audio(sound_file, format="audio/mp3", start_time=0)

# ASK YOUR IMAGE
            st.subheader("Ask your image a question:")


# Get the question from the user
            question = st.text_input("Your question:")


            if st.button("Get Answer") and question:
                params = {"url": input_url, "question": question}
                api_endpoint = f"{base_url}url_answer"
                res = requests.get(api_endpoint, params=params)
                if res.status_code == 200:
                    st.markdown("<p style='font-size:25px; font-family:sans-serif;'>Answer: {}</p>".format(res.json()), unsafe_allow_html=True)



elif choice == "Upload Image":

# # Upload_file:
    uploaded_file = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"]) #Upload photo


    if uploaded_file is not None:
        st.image(uploaded_file, use_column_width=True)
        api_endpoint = f"{base_url}predict_image"
        img = uploaded_file.getvalue()
        files = {'file': img}
        response = requests.post(api_endpoint, files=files)
        if response.status_code == 200:
            caption = response.json()
            st.markdown("<p style='font-size:25px; font-family:sans-serif;'>Caption: {}</p>".format(response.json()), unsafe_allow_html=True)
# Text-to-speech - reading out the caption
            sound_file = BytesIO()
            tts = gTTS(caption, lang='en')
            tts.write_to_fp(sound_file)
            st.audio(sound_file, format="audio/mp3", start_time=0)

# ASK YOUR IMAGE
            st.subheader("Ask your image a question:")

# Get the question from the user
            question = st.text_input("Your question:")


            if st.button("Get Answer") and question:
                files = {"file": img}
                params = {"question":question}
                api_endpoint = f"{base_url}visual_q"
                res = requests.post(api_endpoint, files=files, params=params)
                if res.status_code == 200:
                    st.markdown("<p style='font-size:25px; font-family:sans-serif;'>Answer: {}</p>".format(res.json()), unsafe_allow_html=True)



elif choice == "Take a New Image":

# # Take photo:
    captured_photo = st.camera_input("Take a photo:") #Take photo

    if captured_photo is not None:
        api_endpoint = f"{base_url}predict_image"
        img = captured_photo.getvalue()
        files = {'file': img}
        response = requests.post(api_endpoint, files=files)
        if response.status_code == 200:
            caption = response.json()
            st.markdown("<p style='font-size:25px; font-family:sans-serif;'>Caption: {}</p>".format(response.json()), unsafe_allow_html=True)
# Text-to-speech - reading out the caption
            sound_file = BytesIO()
            tts = gTTS(caption, lang='en')
            tts.write_to_fp(sound_file)
            st.audio(sound_file, format="audio/mp3", start_time=0)

# ASK YOUR IMAGE
            st.subheader("Ask your image a question:")

# Get the question from the user
            question = st.text_input("Your question:")

            if st.button("Get Answer") and question:
                files = {"file": img}
                params = {"question":question}
                api_endpoint = f"{base_url}visual_q"
                res = requests.post(api_endpoint, files=files, params=params)
                if res.status_code == 200:
                    st.markdown("<p style='font-size:25px; font-family:sans-serif;'>Answer: {}</p>".format(res.json()), unsafe_allow_html=True)



else:
    st.write("Choose an option")
