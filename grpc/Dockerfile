FROM python:3.11-slim

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y && \
    apt-get clean -y

RUN pip install --upgrade pip

ENV VIRTUAL_ENV=/app/env

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["tail", "-f", "/dev/null"]

EXPOSE 50051
