# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /home

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app .

CMD ["python","main.py"] 
