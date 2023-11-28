from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from image-captioning.interface.main import open_image, preprocess, generate_caption
app = FastAPI()


# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# @app.get("/predict_upload_image")
# async def put_object(request: requests, file: UploadFile = File(...)) -> str:

#     request_object_content = await file.read()
#     img = Image.open(io.BytesIO(request_object_content))
#     processor = AutoProcessor.from_pretrained("microsoft/git-base-coco")
#     pixel_values = processor(images=img, return_tensors="pt").pixel_values

#     # converting image pixels to ids
#     generated_ids = app.state.model.generate(pixel_values=pixel_values, max_length=50)

#     # generates final caption of image
#     generated_caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

#     return str(generated_caption)


# @app.get("/predict_upload_image_path")
# def predict_upload(image_path):
#     image = Image.open(image_path)
#     app.state.model  = AutoModelForCausalLM.from_pretrained("microsoft/git-base-coco")

#     # preproces the image
#     processor = AutoProcessor.from_pretrained("microsoft/git-base-coco")
#     pixel_values = processor(images=image, return_tensors="pt").pixel_values

#     # converting image pixels to ids
#     generated_ids = app.state.model.generate(pixel_values=pixel_values, max_length=50)

#     # generates final caption of image
#     generated_caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

#     return str(generated_caption)

@app.get("/predict_url")
def predict_caption(url):
    image = open_image(url=url)
    (preprocessor, pixel_values) = preprocess(image)
    caption = generate_caption(preprocessor, pixel_values)
    # image = Image.open(requests.get(url=url, stream=True).raw)
    # app.state.model  = AutoModelForCausalLM.from_pretrained("microsoft/git-base-coco")

    # # preproces the image
    # processor = AutoProcessor.from_pretrained("microsoft/git-base-coco")
    # pixel_values = processor(images=image, return_tensors="pt").pixel_values

    # # converting image pixels to ids
    # generated_ids = app.state.model.generate(pixel_values=pixel_values, max_length=50)

    # # generates final caption of image
    # generated_caption = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return str(caption)

@app.get("/")
def root():
    return {
        'testing' : 'Hello'
        }
