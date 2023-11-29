FROM python:3.10.6-buster

WORKDIR /prod

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY image_captioning image_captioning
COPY setup.py setup.py

RUN pip install .

COPY Makefile Makefile

  CMD uvicorn image_captioning.api.fast:app --host 0.0.0.0 --port $PORT
