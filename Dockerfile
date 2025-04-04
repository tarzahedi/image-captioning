FROM python:3.10.6-buster

WORKDIR /prod

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY image_interface image_interface
COPY Logo_Im_Cap.png Logo_Im_Cap.png
COPY setup.py setup.py

RUN pip install .

COPY Makefile Makefile

CMD uvicorn image_interface.api.fast:app --host 0.0.0.0 --port $PORT
