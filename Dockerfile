FROM python:3.9-slim-buster as base-stage

WORKDIR /app
RUN apt-get update
RUN apt-get install -y git ffmpeg
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt