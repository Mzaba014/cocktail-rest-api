FROM python:3.9-alpine
MAINTAINER Manny

ENV PYTHONUNBUFFERED 1

# copy and install requirements
COPY ./requirements.txt /requirements.txt
# use system package manager to install posgres client. nocache minimizes footprint
RUN apk add --update --no-cache postgresql-client

# create named dependency bundle which we will delete after install, minimizing dependencies
RUN apk add --update --no-cache --virtual .temp-dependencies \
	gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
	
# install requirements
RUN pip install -r /requirements.txt

# uninstall temp-dependencies
RUN apk del .temp-dependencies

# create /app folder on container
RUN mkdir /app

# set /app as workdir in container
WORKDIR /app

# copy app folder from host into app folder on container
COPY ./app/ /app

# create service account to run app instead of root
RUN adduser -D user
USER user

