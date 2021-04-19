#!/usr/bin/env bash

cd /app && \
python wait_for_it.py && \

cd /app/telegram_bot && \
python bot.py