import streamlit as st
from streamlit import session_state as ss
# from gtts import gTTS
# from io import BytesIO
# from IPython.display import Audio
from PIL import Image
import requests



base_url = "https://imagecap-siqf5cui7q-ew.a.run.app/"

# Streamlit app title
st.title(":camera_with_flash: :speech_balloon: :camera_with_flash: :speech_balloon: :camera_with_flash: :speech_balloon: :camera_with_flash: :speech_balloon: :camera_with_flash: :speech_balloon: :camera_with_flash: :speech_balloon: :camera_with_flash:")

# Streamlit app content
st.header("Lets caption some pictures!")

# Add a sidebar to the app
with st.sidebar:
    # Choice selector for the user in the sidebar
    st.markdown("<p style='font-size:20px; font-family:sans-serif; font-weight: bold;color: #523F6D;'>Choose an option:</p>", unsafe_allow_html=True)
    choice = st.radio("", ("Upload Image", "Provide URL", "Take a New Image"))

# Initialize session state
if 'show_uploader' not in ss:
    ss['show_uploader'] = True

if 'image' not in ss:
    ss['image'] = None

# Main content
if choice == "Provide URL":
    # # URL:
    input_url = st.text_input('Upload image via url:')

    if input_url is not None:
        params = {"url": input_url}
        api_endpoint = f"{base_url}predict_url"
        response = requests.get(api_endpoint, params=params)
        if response.status_code == 200:
            image = Image.open(requests.get(input_url, stream=True).raw).convert("RGB")
            st.image(image)
            caption = response.json()
            st.markdown("<p style='font-size:25px; font-family:sans-serif;'>Caption: {}</p>".format(response.json()), unsafe_allow_html=True)
# #TEXT TO SPEECH
#             sound_file = BytesIO()
#             tts = gTTS(caption, lang='en')
#             tts.write_to_fp(sound_file)
#             st.audio(sound_file, format="audio/mp3", start_time=0)

#ASK YOUR IMAGE
            st.title(":camera_with_flash: :grey_question: :camera_with_flash: :grey_question: :camera_with_flash: 	:grey_question: :camera_with_flash: :grey_question: :camera_with_flash: :grey_question: :camera_with_flash: :grey_question: :camera_with_flash:")
            st.header("Now ask your image a question!")
            question = st.text_input("Your question:")

            if st.button("Get Answer") and question:
                params = {"url": input_url, "question": question}
                api_endpoint = f"{base_url}url_answer"
                res = requests.get(api_endpoint, params=params)
                if res.status_code == 200:
                    st.markdown("<p style='font-size:25px; font-family:sans-serif;'>Answer: {}</p>".format(res.json()), unsafe_allow_html=True)

elif choice == "Upload Image":
    # # Upload_file:
    if ss['show_uploader']:
        uploaded_file = st.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])  # Upload photo

        if uploaded_file is not None:
            ss['image'] = uploaded_file  # backup the file
            ss['show_uploader'] = False
            st.rerun()

    if ss['image'] is not None:
        st.image(ss['image'], use_column_width=True)
        api_endpoint = f"{base_url}predict_image"
        img = ss['image'].getvalue()
        files = {'file': img}
        response = requests.post(api_endpoint, files=files)
        if response.status_code == 200:
            caption = response.json()
            st.markdown("<p style='font-size:25px; font-family:sans-serif;'>Caption: {}</p>".format(response.json()), unsafe_allow_html=True)
# #TEXT TO SPEECH
#             sound_file = BytesIO()
#             tts = gTTS(caption, lang='en')
#             tts.write_to_fp(sound_file)
#             st.audio(sound_file, format="audio/mp3", start_time=0)

#ASK YOUR IMAGE
            st.title(":camera_with_flash: :grey_question: :camera_with_flash: :grey_question: :camera_with_flash: 	:grey_question: :camera_with_flash: :grey_question: :camera_with_flash: :grey_question: :camera_with_flash: :grey_question: :camera_with_flash:")
            st.header("Now ask your image a question!")
            question = st.text_input("Your question:")

            if st.button("Get Answer") and question:
                files = {"file": img}
                params = {"question": question}
                api_endpoint = f"{base_url}visual_q"
                res = requests.post(api_endpoint, files=files, params=params)
                if res.status_code == 200:
                    st.markdown("<p style='font-size:25px; font-family:sans-serif;'>Answer: {}</p>".format(res.json()), unsafe_allow_html=True)

elif choice == "Take a New Image":
    # # Take photo:
    captured_photo = st.camera_input("Take a photo:")  # Take photo

    if captured_photo is not None:
        api_endpoint = f"{base_url}predict_image"
        img = captured_photo.getvalue()
        files = {'file': img}
        response = requests.post(api_endpoint, files=files)
        if response.status_code == 200:
            caption = response.json()
            st.markdown("<p style='font-size:25px; font-family:sans-serif;'>Caption: {}</p>".format(response.json()), unsafe_allow_html=True)
# #TEXT TO SPEECH
#             sound_file = BytesIO()
#             tts = gTTS(caption, lang='en')
#             tts.write_to_fp(sound_file)
#             st.audio(sound_file, format="audio/mp3", start_time=0)

 #ASK YOUR IMAGE
            st.title(":camera_with_flash: :grey_question: :camera_with_flash: :grey_question: :camera_with_flash: 	:grey_question: :camera_with_flash: :grey_question: :camera_with_flash: :grey_question: :camera_with_flash: :grey_question: :camera_with_flash:")
            st.header("Now ask your image a question!")
            question = st.text_input("Your question:")

            if st.button("Get Answer") and question:
                files = {"file": img}
                params = {"question": question}
                api_endpoint = f"{base_url}visual_q"
                res = requests.post(api_endpoint, files=files, params=params)
                if res.status_code == 200:
                    st.markdown("<p style='font-size:25px; font-family:sans-serif;'>Answer: {}</p>".format(res.json()), unsafe_allow_html=True)

else:
    st.write("Choose an option")
