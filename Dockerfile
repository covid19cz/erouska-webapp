FROM python:3.7-slim

MAINTAINER jendakolena@gmail.com

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN pip install .

ENTRYPOINT ["covid19-btwa"]
