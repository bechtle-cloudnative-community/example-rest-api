FROM ubuntu:focal

RUN apt update && apt install -y python3 python3-pip
RUN pip3 install waitress

COPY ./requirements.txt /opt/requirements.txt
RUN pip3 install -r /opt/requirements.txt

ENV TZ="Europe/Berlin"

COPY ./src/* /app/

WORKDIR /app
EXPOSE 5000

CMD waitress-serve --port=5000 "main:app" 


# Simple:      docker run -d -p 5001:5000 --name ex_app_1 example_rest-api
# Persistent:  docker run -d -p 5001:5000 -e DATADIR="/data" -v /myhome/vol:/data --name ex_app_1 example_rest-api
