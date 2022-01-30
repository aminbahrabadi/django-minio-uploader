FROM python:3.8-slim-buster
WORKDIR /uploader_project
RUN apt-get update && apt-get install wget unzip zip -y
RUN wget https://dl.min.io/server/minio/release/linux-amd64/minio
RUN chmod +x minio
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .