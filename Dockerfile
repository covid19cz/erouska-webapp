FROM python:3.7-slim AS build_js

MAINTAINER jendakolena@gmail.com

RUN apt-get update
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_13.x | bash -
RUN apt-get install -y nodejs

COPY ./src/btwa_frontend /usr/src/app/src/btwa_frontend
WORKDIR /usr/src/app/src/btwa_frontend

RUN npm ci
RUN npm run build

FROM python:3.7-slim

COPY . /usr/src/app
COPY --from=build_js /usr/src/app/src/btwa_frontend/public /usr/src/app/src/btwa_frontend/public

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl gnupg2 && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y --no-install-recommends unixodbc-dev msodbcsql17 build-essential unixodbc && \
    pip install . && \
    dpkg -P unixodbc-dev build-essential && \
    apt-get -y autoremove && \
    apt-get -y clean && \
    rm -rf /root/.cache /var/lib/apt/lists/*

WORKDIR /usr/src/app/src/btwa_api

ENV WORKER_COUNT 4
ENV PORT 5000

CMD alembic upgrade head && \
    uvicorn main:app --loop uvloop --workers ${WORKER_COUNT} --host 0.0.0.0 --port ${PORT}
