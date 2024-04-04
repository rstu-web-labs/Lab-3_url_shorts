FROM python:3.11-alpine3.19

COPY requirements.txt ./

RUN pip install -r requirements.txt

WORKDIR /app
COPY ./app ./app