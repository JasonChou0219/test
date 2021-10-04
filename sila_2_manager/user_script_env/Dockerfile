FROM python:3

WORKDIR /usr/src/app

RUN pip install --upgrade pip

// RUN apk update
// RUN apk add make automake gcc g++ subversion python3-dev

COPY ./requirements.txt .

COPY ./main.py .

COPY ./SiLA_replacements/ ./SiLA_replacements

COPY ./data/ ./data

COPY ./replace_files.py .

ADD device_layer.tar  .

COPY data_directories.py ./source/device_manager/

RUN pip install --no-cache-dir -r requirements.txt

RUN pip uninstall protobuf -y

RUN pip install --no-binary protobuf protobuf

RUN python replace_files.py
