from transformers import AutoProcessor, AutoModelForCausalLM, ViltProcessor, ViltForQuestionAnswering
from PIL import Image
import requests

def open_image(url=None, image_path=None, img_file_buffer=None):
    '''opens images via url/image path or image upload'''
    # if a url is provided -> retrieve image via url
    if url is not None:
        image = Image.open(requests.get(url=url, stream=True).raw).convert('RGB')
    # else retrieve via an image path
    elif image_path is not None:
        image = Image.open(image_path).convert('RGB')
    # add extra functionality to call camera on laptop
    elif img_file_buffer is not None:
        image = Image.open(img_file_buffer).convert('RGB')
        image = Image.open(img_file_buffer).convert('RGB')
    return image

def preprocess_generated_caption(model, image):
    preprocessor = AutoProcessor.from_pretrained("microsoft/git-base-coco")
    pixel_values = preprocessor(images=image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values=pixel_values, max_length=50)
    generated_caption = preprocessor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_caption

def visual_questioning(image, question):
    processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
    model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
    encoding = processor(image, question, return_tensors="pt")
    outputs = model(**encoding)
    logits = outputs.logits
    idx = logits.argmax(-1).item()
    return model.config.id2label[idx]
