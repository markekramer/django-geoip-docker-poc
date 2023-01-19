# syntax=docker/dockerfile:1
FROM python:3.11-alpine

ENV MAXMIND_VERSION=1.7.1
ENV PYTHONUNBUFFERED=1

COPY GeoLite2-City.mmdb /usr/share/geoip/

RUN pip install --upgrade pip

RUN set -x \
  && apk add --no-cache --virtual .tmp-build-deps \
    alpine-sdk gcc libc-dev linux-headers perl musl-dev zlib zlib-dev \
  && wget https://github.com/maxmind/libmaxminddb/releases/download/${MAXMIND_VERSION}/libmaxminddb-${MAXMIND_VERSION}.tar.gz \
  && tar xf libmaxminddb-${MAXMIND_VERSION}.tar.gz \
  && cd libmaxminddb-${MAXMIND_VERSION} \
  && ./configure \
  && make \
  && make check \
  && make install \
  && apk del .tmp-build-deps


WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY ./src /code/