#!/usr/bin/env bash

cd /app && \
python wait_for_it.py && \
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

