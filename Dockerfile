FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /etc/requirements.txt

RUN mkdir /app
WORKDIR /app
COPY . /app

EXPOSE 8000

RUN pip install -r /etc/requirements.txt

