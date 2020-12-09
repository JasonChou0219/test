FROM python:3.8


WORKDIR /usr/src/app

COPY ./requirements.txt .

COPY ./main.py .

#COPY ../source/device_manager/device_layer .
ADD device_layer.tar  .

RUN pip install --no-cache-dir -r requirements.txt


