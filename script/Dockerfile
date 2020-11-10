FROM python:3.7.5-stretch

COPY ./test /src/test
COPY ./requirements.txt /src/
COPY ./*.py /src/
COPY ./run.sh /

RUN apt-get update -y && apt-get install zip -y && pip install virtualenv
