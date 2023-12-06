import time
from io import BytesIO

import requests
import speech_recognition as sr  # (SpeechRecognition in pypi)
import streamlit as st
from gtts import gTTS
from PIL import Image
from streamlit import session_state as ss
from streamlit_option_menu import option_menu


def transcribe_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        # with st.spinner("Listening..."):
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            st.write("Could not understand audio")
        except sr.RequestError as e:
            st.write(
                "Could not request results from Google Speech Recognition service; {0}"
                .format(e))


base_url = "http://127.0.0.1:8000/"
#base_url = "https://imagecap-siqf5cui7q-ew.a.run.app/"

# Streamlit app title
st.title(":camera_with_flash: :speech_balloon: Let's Caption Your Image")

# Add a sidebar to the app
with st.sidebar:
    st.image("Logo_Im_Cap.png", use_column_width=True)
    # Choice selector for the user in the sidebar
    selected = option_menu(
        "Main Menu",
        ["Home", "Upload Image", 'Provide URL', "Take a New Image"],
        icons=['house', 'gear', 'eye', 'camera'],
        default_index=1)
    selected

## HOME PAGE

if selected == "Home":
    st.header("Caption your pictures")
    st.write(
        "Welcome to a world where innovation meets inclusivity! We believe in bridging the visual gap and providing a virtual window to the world. With our cutting-edge AI, you're not just decoding pixels; you're unlocking a universe of possibilities. Our mission is to redefine accessibility."
    )

    st.subheader("Get detailed descriptions of your images")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR2ew7u6dEGWAZWQJcjZ5yofPZuWdwuKJb2HRch22JR8yyIlSLDW29nHzWMFuw2pG01X-A&usqp=CAU"
        )
        st.write("Caption: dogs on the beach")
    with col2:

        st.image(
            "https://media-cldnry.s-nbcnews.com/image/upload/newscms/2017_03/1868126/ss-170117-men-who-walked-moon-duke-mn-11.jpg"
        )
        st.write("Caption: astronaut on the moon during space mission")
    with col3:

        st.image(
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_mVdZJqudtSUtFyZfoUUZj74P_Y8Lv3GKlQ&usqp=CAU"
        )
        st.write(
            "Caption: football player celebrates after scoring a goal during the final against football team"
        )

    st.subheader("And ask your image questions")
    st.write(
        "Our AI tool transforms the passive act of viewing into an interactive exploration, allowing you to inquire about the details that matter most to you. Start asking it directly!"
    )

## UPLOAD URL
if selected == "Provide URL":
    input_url = st.text_input('Upload image via url:')

    if input_url is not None:
        if len(input_url) > 0:
            with st.spinner("Loading..."):
                params = {"url": input_url}
                api_endpoint = f"{base_url}predict_url"
                response = requests.get(api_endpoint, params=params)
                if response.status_code == 200:
                    image = Image.open(
                        requests.get(input_url,
                                     stream=True).raw).convert("RGB")
                    st.image(image)
                    caption = response.json()
                    st.markdown(
                        "<p style='font-size:25px; font-family:sans-serif;'>Caption: {}</p>"
                        .format(response.json()),
                        unsafe_allow_html=True)
                    #TEXT TO SPEECH - Caption
                    sound_file = BytesIO()
                    tts = gTTS(caption, lang='en')
                    tts.write_to_fp(sound_file)
                    st.audio(sound_file, format="audio/mp3", start_time=0)

                    #ASK YOUR IMAGE
                    st.title(
                        ":camera_with_flash: :grey_question: Now Ask It a Question:"
                    )

                    genre = st.radio("", ["Voice", "Text"], horizontal=True)

                    if genre == "Text":
                        question = st.text_input("Your question:")
                        if st.button("Get Answer") and question:
                            params = {"url": input_url, "question": question}
                            api_endpoint = f"{base_url}url_answer"
                            res = requests.get(api_endpoint, params=params)
                            if res.status_code == 200:
                                answer = res.json()
                                st.markdown(
                                    "<p style='font-size:25px; font-family:sans-serif;'>Answer: {}</p>"
                                    .format(res.json()),
                                    unsafe_allow_html=True)
                                #TEXT TO SPEECH - Answer
                                sound_file = BytesIO()
                                tts = gTTS(answer, lang='en')
                                tts.write_to_fp(sound_file)
                                st.audio(sound_file,
                                         format="audio/mp3",
                                         start_time=0)

        #SPEECH TO TEXT - Question

                    elif genre == "Voice":
                        ready_button = st.button("Ask your question",
                                                 key='ready_button')
                        if ready_button:
                            with st.spinner("Listening..."):
                                text = transcribe_speech()
                                time.sleep(1)
                            if text:
                                st.write(f"Question: {text}?")
                                params = {
                                    "url": input_url,
                                    "question": f"{text}?"
                                }
                                api_endpoint = f"{base_url}url_answer"
                                res = requests.get(api_endpoint, params=params)
                                if res.status_code == 200:
                                    answer = res.json()
                                    st.markdown(
                                        "<p style='font-size:25px; font-family:sans-serif;'>Answer: {}</p>"
                                        .format(res.json()),
                                        unsafe_allow_html=True)
                                    #TEXT TO SPEECH - Answer
                                    sound_file = BytesIO()
                                    tts = gTTS(answer, lang='en')
                                    tts.write_to_fp(sound_file)
                                    st.audio(sound_file,
                                             format="audio/mp3",
                                             start_time=0)

## UPLOAD IMAGE
elif selected == "Upload Image":
    uploaded_file = st.file_uploader("Upload an image:",
                                     type=["jpg", "jpeg",
                                           "png"])  # Upload photo

    if uploaded_file is not None:
        with st.spinner("Loading..."):
            api_endpoint = f"{base_url}predict_image"
            img = uploaded_file.getvalue()
            files = {'file': img}
            response = requests.post(api_endpoint, files=files)
            if response.status_code == 200:
                st.image(uploaded_file, use_column_width=True)
                caption = response.json()
                st.markdown(
                    "<p style='font-size:25px; font-family:sans-serif;'>Caption: {}</p>"
                    .format(caption),
                    unsafe_allow_html=True)

                #TEXT TO SPEECH - Caption
                sound_file = BytesIO()
                tts = gTTS(caption, lang='en')
                tts.write_to_fp(sound_file)
                st.audio(sound_file, format="audio/mp3", start_time=0)

                #ASK YOUR IMAGE
                st.title(
                    ":camera_with_flash: :grey_question: Now Ask It a Question:"
                )

                genre = st.radio("", ["Voice", "Text"], horizontal=True)

                if genre == "Text":
                    question = st.text_input("Your question:")

                    if st.button("Get Answer") and question:
                        files = {"file": img}
                        params = {"question": question}
                        api_endpoint = f"{base_url}visual_q"
                        res = requests.post(api_endpoint,
                                            files=files,
                                            params=params)
                        if res.status_code == 200:
                            answer = res.json()
                            st.markdown(
                                "<p style='font-size:25px; font-family:sans-serif;'>Answer: {}</p>"
                                .format(res.json()),
                                unsafe_allow_html=True)
                            #TEXT TO SPEECH - Answer
                            sound_file = BytesIO()
                            tts = gTTS(answer, lang='en')
                            tts.write_to_fp(sound_file)
                            st.audio(sound_file,
                                     format="audio/mp3",
                                     start_time=0)

                elif genre == "Voice":
                    ready_button = st.button("Ask your question",
                                             key='ready_button')

                    if ready_button:
                        with st.spinner("Listening..."):
                            text = transcribe_speech()
                            time.sleep(1)

                        if text:
                            st.write(f"Question: {text}?")
                            files = {"file": img}
                            params = {"question": f"{text}?"}
                            api_endpoint = f"{base_url}visual_q"
                            res = requests.post(api_endpoint,
                                                files=files,
                                                params=params)
                            if res.status_code == 200:
                                answer = res.json()
                                st.markdown(
                                    "<p style='font-size:25px; font-family:sans-serif;'>Answer: {}</p>"
                                    .format(res.json()),
                                    unsafe_allow_html=True)
                                #TEXT TO SPEECH - Answer
                                sound_file = BytesIO()
                                tts = gTTS(answer, lang='en')
                                tts.write_to_fp(sound_file)
                                st.audio(sound_file,
                                         format="audio/mp3",
                                         start_time=0)

## TAKE A NEW IMAGE
elif selected == "Take a New Image":
    captured_photo = st.camera_input("Take a photo:")  # Take photo

    if captured_photo is not None:
        with st.spinner("Loading..."):
            api_endpoint = f"{base_url}predict_image"
            img = captured_photo.getvalue()
            files = {'file': img}
            response = requests.post(api_endpoint, files=files)
            if response.status_code == 200:
                caption = response.json()
                st.markdown(
                    "<p style='font-size:25px; font-family:sans-serif;'>Caption: {}</p>"
                    .format(response.json()),
                    unsafe_allow_html=True)
                #TEXT TO SPEECH - Caption
                sound_file = BytesIO()
                tts = gTTS(caption, lang='en')
                tts.write_to_fp(sound_file)
                st.audio(sound_file, format="audio/mp3", start_time=0)

                #ASK YOUR IMAGE
                st.title(
                    ":camera_with_flash: :grey_question: Now Ask It a Question:"
                )

                genre = st.radio("", ["Voice", "Text"], horizontal=True)

                if genre == "Text":

                    question = st.text_input("Your question:")

                    if st.button("Get Answer") and question:
                        files = {"file": img}
                        params = {"question": question}
                        api_endpoint = f"{base_url}visual_q"
                        res = requests.post(api_endpoint,
                                            files=files,
                                            params=params)
                        if res.status_code == 200:
                            answer = res.json()
                            st.markdown(
                                "<p style='font-size:25px; font-family:sans-serif;'>Answer: {}</p>"
                                .format(res.json()),
                                unsafe_allow_html=True)
                            #TEXT TO SPEECH - Answer
                            sound_file = BytesIO()
                            tts = gTTS(answer, lang='en')
                            tts.write_to_fp(sound_file)
                            st.audio(sound_file,
                                     format="audio/mp3",
                                     start_time=0)

                elif genre == "Voice":
                    ready_button = st.button("Ask your question",
                                             key='ready_button')

                    if ready_button:
                        with st.spinner("Listening..."):
                            text = transcribe_speech()
                            time.sleep(1)

                        if text:
                            st.write(f"Question: {text}?")
                            files = {"file": img}
                            params = {"question": f"{text}?"}
                            api_endpoint = f"{base_url}visual_q"
                            res = requests.post(api_endpoint,
                                                files=files,
                                                params=params)
                            if res.status_code == 200:
                                answer = res.json()
                                st.markdown(
                                    "<p style='font-size:25px; font-family:sans-serif;'>Answer: {}</p>"
                                    .format(res.json()),
                                    unsafe_allow_html=True)
                                #TEXT TO SPEECH - Answer
                                sound_file = BytesIO()
                                tts = gTTS(answer, lang='en')
                                tts.write_to_fp(sound_file)
                                st.audio(sound_file,
                                         format="audio/mp3",
                                         start_time=0)
