FROM python:3.8-slim

# Python application
ENV PYTHONBUFFERED 1
ENV APPLICATION_ROOT /app/
RUN mkdir -p $APPLICATION_ROOT
WORKDIR $APPLICATION_ROOT
RUN pip install pipenv

COPY Pipfile /app
COPY Pipfile.lock /app
RUN pipenv install --system

ADD . /app
COPY wait-for-it.sh /app
