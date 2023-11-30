from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoModelForCausalLM
from image_interface.interface.main import open_image, preprocess_generated_caption, visual_questioning
from PIL import Image
from io import BytesIO

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

        caption = preprocess_generated_caption(app.state.model, image)

        return str(caption)



@app.get("/predict_url")
def predict_caption(url):
    image = open_image(url=url)
    caption = preprocess_generated_caption(app.state.model, image)

    return str(caption)

@app.get("visual_q")
def get_answer(img_file_buffer, question):
    image = open_image(img_file_buffer)
    answer = visual_questioning(image, question)
    return answer

@app.get("/")
def root():
    return {
        'testing' : 'Hello'
        }
