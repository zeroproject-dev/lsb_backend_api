# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.7.9 AS builder
RUN apt update && apt-get install -y git default-libmysqlclient-dev build-essential ffmpeg

WORKDIR /code
COPY requirements.txt /code
RUN --mount=type=cache,target=/root/.cache/pip \
  pip3 install -r requirements.txt

COPY . .

ENV FLASK_APP src/main.py
ENV ENV prod 
ENV JWT_KEY bJHYd7M8sYoTgdCLBryz^eg&Hz2&wN4N

EXPOSE 3300

# CMD ["flask", "run"]
CMD ["python3", "src/main.py"]
