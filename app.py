import streamlit as st
import pandas as pd
from io import StringIO
from PIL import Image
import requests
from gtts import gTTS
from io import BytesIO


# Streamlit app title
st.title("Image Captioning")

# Streamlit app content
st.header("Lets caption some pictures!")

# File uploader widget
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Check if a file is uploaded
if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, use_column_width=True)

    # Process the uploaded image using PIL
    image = Image.open(uploaded_file)

    # API endpoint for your FastAPI app
    api_endpoint = "http://your-fastapi-app-endpoint/predict"  # Replace with your actual FastAPI endpoint

    # Make an API request to get the image caption
    response = requests.post(api_endpoint, files={"image": uploaded_file})
    if response.status_code == 200:
        caption = response.json().get("caption", "Caption not available")

        # Display the generated caption in the Streamlit UI
        st.write("Image Caption:", caption)

        # Text-to-speech - reading out the caption
        sound_file = BytesIO()
        tts = gTTS(caption, lang='en')
        tts.write_to_fp(sound_file)
        st.audio(sound_file, format="audio/mp3", start_time=0)
    else:
        st.error("Error processing the image. Please try again.")
