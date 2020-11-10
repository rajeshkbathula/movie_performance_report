RUN_TEST: test main
RUN_IN_DOCKER: test-with-mysql main-with-mysql
PYTHON?=


WORK_DIR=$(shell pwd)
PYTHON               ?=python # change here how you set bash profile your python like python3 or python
PIP_VERSION             ?=PIP
#TMP_CW_LOKI_SHIPPER         ?=/tmp/$(LOKI_SHIPPER)

local_test:
	cd script && virtualenv ./.venv; \
	source ./.venv/bin/activate; $(PIP_VERSION) install -r ./requirements.txt; \
	PYTHON ./test/test_main_script.py

docker-build:
#	rm -rf $(TMP_CW_LOKI_SHIPPER)
#	cp -r ${WORK_DIR}/$(CW_LOKI_SHIPPER) $(TMP_CW_LOKI_SHIPPER)
	cd $(TMP_CW_LOKI_SHIPPER) && virtualenv ./.venv; \
	source ./.venv/bin/activate; $(PIP_VERSION) install -r ./requirements.txt; \
	$(PIP_VERSION) install pytest; pytest ./test; $(PIP_VERSION) install -r ./requirements.txt -t ./; \
	sh ./build

docker-build:
	docker build ./ -t mysql-db
	docker run --env="MYSQL_ROOT_PASSWORD=root_password" -p 3306:3306 -d mysql-db
	sleep 20

test:
	.venv/bin/pytest tests/json_to_agrt_main_test.py -v

main-with-mysql:
	.venv/bin/python ./main/json_format_push_to_mysql.py --db='presentation_db'

main: test
	.venv/bin/python ./main/json_format_push_to_mysql.py

wtest-with-mysql:
	.venv\Scripts\pytest .\tests -v

wtest:
	.venv\Scripts\pytest .\tests\json_to_agrt_main_test.py -v

wmain-with-mysql: wtest-with-mysql
	.venv\Scripts\python .\main\json_format_push_to_mysql.py --db='presentation_db'

wmain: wtest
	.venv\Scripts\python .\main\json_format_push_to_mysql.py
