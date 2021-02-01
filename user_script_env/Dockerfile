FROM python:3.8


WORKDIR /usr/src/app

COPY ./requirements.txt .

COPY ./main.py .

ADD device_layer.tar  .

COPY data_directories.py ./source/device_manager/

RUN pip install --no-cache-dir -r requirements.txt