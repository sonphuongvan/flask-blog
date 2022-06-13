# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /flask_blog
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ENV app=dev
COPY . .
CMD [ "/usr/local/bin/python", "run.py"]
