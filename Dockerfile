FROM python:3.12.1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
ADD . /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app