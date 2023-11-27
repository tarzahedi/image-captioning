import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoProcessor, AutoModelForCausalLM
import requests
from PIL import Image
app = FastAPI()
app.state.model = AutoModelForCausalLM.from_pretrained("microsoft/git-base-coco")


# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/predict")
def predict(url):
    image = Image.open(requests.get(url=url, stream=True).raw)
    app.state.model  = AutoModelForCausalLM.from_pretrained("microsoft/git-base-coco")

    # preproces the image
    processor = AutoProcessor.from_pretrained("microsoft/git-base-coco")
    pixel_values = processor(images=image, return_tensors="pt").pixel_values

    # converting image pixels to ids
    generated_ids = app.state.model.generate(pixel_values=pixel_values, max_length=50)

    # generates final caption of image
    generated_caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return str(generated_caption)

@app.get("/")
def root():
    return {
        'testing' : 'Hello'
        }
