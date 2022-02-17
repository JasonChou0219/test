FROM python:3

WORKDIR /usr/src/app

RUN pip install --upgrade pip

COPY ./requirements.txt .
COPY ./main.py .
COPY ./data/ ./data
COPY data_directories.py .

RUN pip install --no-cache-dir -r requirements.txt
