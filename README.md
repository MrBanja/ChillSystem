# Chill System

### Table of content
* [About](#about)
* [How to](#how-to)
* [About technical details](#about-technical-details)
    * [Telegram Bot](#telegram-bot)
    * [Web service](#web-service)
* [Deploy](#deploy)

## About

It is a system for those who are lazy. 
Imagine, you have an old TV or a computer monitor. Your friend come to
your party and you would like to watch some youtube videos with your
pals. But the TV is old enough to support YouTube app (monitor can not 
do it at all). 

There is the solution! **Chill System**. Just connect you laptop or PC to
an TV(monitor) or open a special web page. Do not worry, you won't stand up
to turn on or skip the video. Now you can use the special _telegram_ bot! Just share
videos from mobile YouTube app to telegram bot. It will add to a queue them automatically
and will play them for you on the web page you opened previously.

## How to
When MVP milestone will be added this section will be expanded.

## About Technical details

This project currently contains telegram bot and a back-end web-service.

**Stack that we are using now**: python3.8+, asyncio(lots of it), FastAPI(as main web-service),
aiohttp(as Client side), Redis(for storing queues, planning to move to the RabbitMQ), Docker.

### Telegram Bot

For the sake of learning this bot was written by me (Mb for production
special package will be used).

It was written with asyncio and aiohttp for telegram api queries.

In future it will be moved to the package as a third-party library.

### Web service

Web service is written on FastAPI. 
Currently it handles webHook from telegram API and web socket connection with a front.


## Deploy

Currently its running with uvicorn ASGI.

In the nearest future will be created dockers images for Web-service with the bot
and for Redis, which will be connected by the docker-compose.

When docker images will be created this section will be expanded.


## Developers

Project was initialy developed and maintained by [Dennis Dobrovolsky](https://github.com/AngliD).
