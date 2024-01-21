FROM python:3.11-slim

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y pkg-config python3-dev default-libmysqlclient-dev build-essential && \
    apt-get clean -y

RUN pip install --upgrade pip

ENV VIRTUAL_ENV=/app/env

COPY /src/requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
