FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r requirements.txt