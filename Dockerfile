FROM python:3.7.3-stretch
RUN apt-get update
RUN apt-get --yes install python3-dev
ENV TZ Europe/Helsinki

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
