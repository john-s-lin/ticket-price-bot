FROM python:alpine as base

COPY . /app

VOLUME ["/logs"]

RUN apk update && \
    apk add bash zsh make musl-dev

WORKDIR /app

RUN pip install -r requirements.txt

FROM base as dev

ENTRYPOINT [ "/bin/bash" ]