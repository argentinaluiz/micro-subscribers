# syntax=docker/dockerfile:1
FROM python:3.9-alpine3.13

RUN apk add --no-cache make bash nodejs npm postgresql-dev gcc python3-dev musl-dev libffi-dev

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1
ENV PIPENV_VENV_IN_PROJECT=1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
#ENV PIP_TARGET=/home/python/app/venv
#ENV PYTHONPATH=/home/python/app/venv
#ENV PATH $PATH:/home/python/app/venv/bin
ENV PATH $PATH:/home/python/app/.venv/bin

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN adduser --disabled-password --uid 1000 python

RUN pip install pipenv

USER python

RUN mkdir /home/python/app

WORKDIR /home/python/app

RUN echo "source /home/python/app/.venv/bin/activate" > /home/python/.bashrc

RUN pipenv install


# pipenv install mozilla-django-oidc
# apk add libffi-dev
# CRYPTOGRAPHY_DONT_BUILD_RUST=1 