FROM python:3.7-slim

MAINTAINER jendakolena@gmail.com

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update \
 && apt-get install -y curl \
 && curl -sL https://deb.nodesource.com/setup_13.x | bash - \
 && apt-get install -y nodejs \
 && cd src/btwa_frontend \
 && npm i \
 && npm run build \
 && cd ../.. \
 && pip install . \
 && apt-get purge -y nodejs curl \
 && apt-get autoremove -y \
 && rm -rf * /var/lib/apt/lists/*

ENTRYPOINT ["covid19-btwa"]
