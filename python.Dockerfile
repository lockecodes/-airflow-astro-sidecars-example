FROM python:3.8-slim

WORKDIR /app

RUN pip install click

COPY src/sidecar_daemon.py .
COPY src/file_creator.py .
