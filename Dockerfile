FROM python:3.7-slim AS build_js

MAINTAINER jendakolena@gmail.com

RUN apt-get update
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_13.x | bash -
RUN apt-get install -y nodejs

COPY ./src/btwa_frontend /usr/src/app/src/btwa_frontend
WORKDIR /usr/src/app/src/btwa_frontend

RUN npm i
RUN npm run build

FROM python:3.7-slim AS build_python

COPY . /usr/src/app
COPY --from=build_js /usr/src/app/src/btwa_frontend/public /usr/src/app/src/btwa_frontend/public
WORKDIR /usr/src/app
RUN pip wheel --no-deps -w /pkgs .

FROM python:3.7-slim

COPY --from=build_python /pkgs/bluetooth_tracing_web_app* /pkgs/
RUN pip install /pkgs/bluetooth_tracing_web_app* && rm -rf ~/.cache

CMD ["covid19-btwa"]
