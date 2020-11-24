FROM ubuntu:latest

RUN apt-get update \
# Python3
    && apt-get install -y python3-pip python3-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip \
# libs for notifBot
    && pip install python-telegram-bot \
    && pip install oauthlib \
    && pip install requests-oauthlib

COPY /app /home/app
WORKDIR /home/app

CMD python3 main.py