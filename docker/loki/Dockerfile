FROM python:3.7-slim

ARG LOKI_VERSION=2.0.0
ARG LOKI_URL="https://github.com/grafana/loki/releases/download/v$LOKI_VERSION/loki-linux-amd64.zip"
#ARG LK_UID="472"
#ARG LK_GID="472"

ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    LK_PATHS_HOME="/usr/bin" \
    LK_PATHS_CONFIG="/loki"

RUN apt-get update && apt-get install -qq -y tar libfontconfig curl ca-certificates unzip && \
    cd $LK_PATHS_HOME && \
    curl -fSL -o loki.zip "$LOKI_URL" && \
    unzip loki.zip && \
    mv loki-linux-amd64 loki && \
    chmod a+x loki && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p "$LK_PATHS_CONFIG"

COPY ./loki.yaml /etc/config/loki.yaml
EXPOSE 3100
