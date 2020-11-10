FROM grafana/loki:v1.3.0

COPY ./loki.yaml /etc/config/loki.yaml


RUN apk add make unzip zip wget
RUN PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip && pip3 install --no-cache --upgrade pip setuptools && pip3 install virtualenv
