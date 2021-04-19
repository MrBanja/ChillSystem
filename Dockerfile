FROM python:3.9

RUN apt-get update && apt-get install -y libpq-dev gcc

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /etc/requirements.txt

RUN mkdir /app
RUN mkdir /app/logs
WORKDIR /app
COPY . /app

RUN pip3 install -r /etc/requirements.txt

