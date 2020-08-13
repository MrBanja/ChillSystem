#!/usr/bin/env bash

cd /app && \
python wait_for_it.py && \

cd /app/workers && \
python web_socket_worker.py
