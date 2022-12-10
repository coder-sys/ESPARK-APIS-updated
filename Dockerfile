# syntax=docker/dockerfile:1
FROM python:3.8-bullseye

WORKDIR /build

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn -w $NUM_WORKERS --timeout $TIMEOUT --bind $HOST:$PORT app:app
