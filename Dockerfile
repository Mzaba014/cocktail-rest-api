FROM python:3.9-alpine
MAINTAINER Manny

ENV PYTHONUNBUFFERED 1

# copy and install requirements
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# create /app folder on container
RUN mkdir /app

# set /app as workdir in container
WORKDIR /app

# copy app folder from host into app folder on container
COPY ./app/ /app

# create service account to run app instead of root
RUN adduser -D user
USER user

