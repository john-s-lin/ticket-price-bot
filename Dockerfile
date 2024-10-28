FROM ghcr.io/astral-sh/uv:alpine AS base

COPY . /app

VOLUME ["/logs"]

RUN apk update &&\
    apk add bash make musl-dev python3~=3.12

WORKDIR /app

RUN uv venv -p 3.12

RUN uv pip sync pyproject.toml

FROM base AS dev

RUN apk add curl git zsh

# Ref: [Unattended ohmyzsh install](https://github.com/ohmyzsh/ohmyzsh?tab=readme-ov-file#unattended-install)
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

ENTRYPOINT [ "/bin/bash" ]
