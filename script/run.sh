#!/bin/sh
set -xe

cd /src/
virtualenv .venv;
    source ./.venv/bin/activate; \
    pip3 install --no-cache-dir -r ./requirements.txt; \
	pytest ./test/; \
	python ./main.py
