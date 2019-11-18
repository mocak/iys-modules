FROM python:alpine
MAINTAINER Murat Ocak <mehmetmuratocak@gmail.com>

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .