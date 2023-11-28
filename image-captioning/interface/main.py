from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import requests

def open_image(url=None, image_path=None):
    # if a url is provided -> retrieve image via url
    if len(url) > 0:
        image = Image.open(requests.get(url=url, stream=True).raw)
    # else retrieve via an image path
    elif len(image_path) > 0:
        image = Image.open(image_path)
    # add extra functionality to call camera on laptop
    return image

def preprocess(image):
    preprocessor = AutoProcessor.from_pretrained("microsoft/git-base-coco")
    pixel_values = preprocessor(images=image, return_tensors="pt").pixel_values
    return (preprocessor, pixel_values)

def generate_caption(preprocessor, pixel_values):
    model = AutoModelForCausalLM.from_pretrained("microsoft/git-base-coco")
    generated_ids = model.generate(pixel_values=pixel_values, max_length=50)
    generated_caption = preprocessor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_caption
