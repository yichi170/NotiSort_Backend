# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:5000 server-flask:app