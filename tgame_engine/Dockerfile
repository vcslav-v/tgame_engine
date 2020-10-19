FROM python:3.7-slim

RUN pip install poetry

RUN mkdir -p /usr/src/app/tgame

ENV CONTAINER_HOME=/usr/src/app/tgame

ADD . $CONTAINER_HOME
WORKDIR $CONTAINER_HOME

RUN poetry install --no-dev 
