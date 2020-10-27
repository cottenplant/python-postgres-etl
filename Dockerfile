FROM python:3.8-slim-buster

ENV LANG C.UTF-8

WORKDIR /app

RUN apt-get update -qq && apt-get install -qqy --no-install-recommends \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    build-essential \
    python3-dev \
    tree

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r /app/requirements.txt

COPY . /app