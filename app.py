import streamlit as st
# import pandas as pd
# from io import StringIO
from PIL import Image
import requests
#import time
# from gtts import gTTS
# from io import BytesIO
#from image_interface.interface.main import open_image,preprocess,generate_caption
# from fastapi import FastAPI, File, UploadFile
# from typing import Annotated
# from image_interface.api.fast import predict_caption, predict_upload

# Streamlit app title
st.title("Image Captioning")

# Streamlit app content
st.header("Lets caption some pictures!")
#st.write("This is :blue[test]")

# Choice selector for the user
choice = st.radio("Choose an option:", ("Upload Image", "Provide URL", "Take a New Image"))

if choice == "Provide URL":

# # URL:
    input_url = st.text_input('put url')

    if input_url is not None:
            # image = Image.open(requests.get(input_url, stream=True).raw).convert("RGB")
            # st.image(image)
        params = {"url": input_url}
        api_endpoint = "http://127.0.0.1:8000/predict_url"

               # Use st.spinner to indicate progress
        #with st.spinner('Processing image...'):
        response = requests.get(api_endpoint, params=params)
            #time.sleep (4)

        if response.status_code == 200:
            image = Image.open(requests.get(input_url, stream=True).raw).convert("RGB")
            st.image(image)
            st.write("Caption: ", response.json())


elif choice == "Upload Image":

# # Upload_file:
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"]) #Upload photo


    if uploaded_file is not None:
        st.image(uploaded_file, use_column_width=True)
        api_endpoint = "http://127.0.0.1:8000/predict_image"
        img = uploaded_file.getvalue()
        files = {'file': img}
        response = requests.post(api_endpoint, files=files)
        if response.status_code == 200:
            st.write("Caption: ", response.json())

elif choice == "Take a New Image":

# # Take photo:
    captured_photo = st.camera_input("Choose an image...") #Take photo

    if captured_photo is not None:
        api_endpoint = "http://127.0.0.1:8000/predict_image"
        img = captured_photo.getvalue()
        files = {'file': img}
        response = requests.post(api_endpoint, files=files)
        if response.status_code == 200:
            st.write("Caption: ", response.json())


else:
    st.write("Choose an option")



# File uploader widget
# uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# # Check if a file is uploaded
# if uploaded_file is not None:
#     # Display the uploaded image
#     st.image(uploaded_file, use_column_width=True)

#     #Process the uploaded image using PIL
#     caption = predict_upload(img_file_buffer=uploaded_file)

#    # Process the uploaded image using PIL
#     #image = Image.open(uploaded_file)

#     # API endpoint for your FastAPI app
#     #api_endpoint = "http://your-fastapi-app-endpoint/predict"  # Replace with your actual FastAPI endpoint

#     # Make an API request to get the image caption
#     # response = requests.get(api_endpoint, files={"image": uploaded_file})
#     # if response.status_code == 200:
#     #     caption = response.json().get("caption", "Caption not available")

#     #     # Display the generated caption in the Streamlit UI
#     #     st.write("Image Caption:", caption)

#     #     # Text-to-speech - reading out the caption
#     #     sound_file = BytesIO()
#     #     tts = gTTS(caption, lang='en')
#     #     tts.write_to_fp(sound_file)
#     #     st.audio(sound_file, format="audio/mp3", start_time=0)

#     #     # Subheader for asking questions
#     #     st.subheader("Ask your image a question:")

#     #     # Ask a question input widget
#     #     question = st.text_input("")

#     #     # Check if a question is asked
#     #     if question:
#     #         # Assume another API endpoint for image question answering
#     #         qa_api_endpoint = "http://your-question-answering-api-endpoint/answer"  # Replace with your actual QA API endpoint

#     #         # Make an API request to get the answer
#     #         qa_response = requests.get(qa_api_endpoint, json={"image": uploaded_file, "question": question})
#     #         if qa_response.status_code == 200:
#     #             answer = qa_response.json().get("answer", "Answer not available")

#     #             # Display the answer in the Streamlit UI
#     #             st.write("Answer:", answer)
#     #         else:
#     #             st.error("Error processing the question. Please try again.")
# else:
#     st.error("Error processing the image. Please try again.")
