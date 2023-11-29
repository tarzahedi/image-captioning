from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from image_captioning.interface.main import open_image, preprocess, generate_caption
app = FastAPI()


# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/predict_image")
def predict_upload(img_file_buffer):
    image = open_image(img_file_buffer=img_file_buffer)
    (preprocessor, pixel_values) = preprocess(image)
    caption = generate_caption(preprocessor, pixel_values)

    return str(caption)

@app.get("/predict_upload")
def predict_upload(image_path):
    image = open_image(image_path=image_path)
    (preprocessor, pixel_values) = preprocess(image)
    caption = generate_caption(preprocessor, pixel_values)

    return str(caption)

@app.get("/predict_url")
def predict_caption(url):

    image = open_image(url=url)
    (preprocessor, pixel_values) = preprocess(image)
    caption = generate_caption(preprocessor, pixel_values)

    return str(caption)

@app.get("/")
def root():
    return {
        'testing' : 'Hello'
        }
