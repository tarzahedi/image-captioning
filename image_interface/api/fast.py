from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoProcessor, AutoModelForCausalLM, ViltProcessor, ViltForQuestionAnswering
# from image_interface.interface.main import open_image, preprocess_generated_caption, visual_questioning
from PIL import Image
from io import BytesIO
import requests

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


@app.post("/predict_image")
async def create_upload_file(file: UploadFile):
    if not file:
        return {"message": "No upload file sent"}
    else:
        contents = await file.read()
        image = Image.open(BytesIO(contents)).convert("RGB")

        preprocessor = AutoProcessor.from_pretrained("microsoft/git-base-coco")
        pixel_values = preprocessor(images=image, return_tensors="pt").pixel_values
        generated_ids = app.state.model.generate(pixel_values=pixel_values, max_length=50)
        generated_caption = preprocessor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return str(generated_caption)




@app.get("/predict_url")
def predict_caption(url):
    image = Image.open(requests.get(url=url, stream=True).raw).convert('RGB')
    preprocessor = AutoProcessor.from_pretrained("microsoft/git-base-coco")
    pixel_values = preprocessor(images=image, return_tensors="pt").pixel_values
    generated_ids = app.state.model.generate(pixel_values=pixel_values, max_length=50)
    generated_caption = preprocessor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return str(generated_caption)




@app.get("/url_answer")
def url_answer(url, question):
    image = Image.open(requests.get(url=url, stream=True).raw).convert('RGB')
    processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
    model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
    encoding = processor(image, question, return_tensors="pt")
    outputs = model(**encoding)
    logits = outputs.logits
    idx = logits.argmax(-1).item()
    output = model.config.id2label[idx]
    return str(output)

@app.post("/visual_q")
async def create_upload_file(file: UploadFile, question):
    if not file:
        return {"message": "No upload file sent"}
    else:
        contents = await file.read()
        image = Image.open(BytesIO(contents)).convert("RGB")

        processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
        model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
        encoding = processor(image, question, return_tensors="pt")
        outputs = model(**encoding)
        logits = outputs.logits
        idx = logits.argmax(-1).item()
        output = model.config.id2label[idx]
        return str(output)


@app.get("/")
def root():
    return {
        'testing' : 'Hello'
        }
