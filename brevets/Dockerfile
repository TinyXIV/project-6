FROM python:3.8
LABEL maintainer="jmuzi04@gmail.com"
RUN apt-get update -y
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
