RUN_TEST: test main
RUN_IN_DOCKER: test-with-mysql main-with-mysql

WORK_DIR=$(shell pwd)
PYTHON       ?=python # change here how you set bash profile your python like python3 or python
PIP_VERSION  ?=PIP
MOUNT_VOLUME ?=/tmp/movies_data
LOKI_URL     ?=http://localhost:9000/explore?orgId=1&left=%5B%22now-1h%22,%22now%22,%22loki%22,%7B%7D%5D


local_test:
	cd script && virtualenv ./.venv; \
	source ./.venv/bin/activate;  $(PIP_VERSION) install -r ./requirements.txt; \
	pytest ./test/test_main_script.py

docker_up:
	cd ./docker && docker-compose up -d

docker_down:
	cd ${WORK_DIR}/docker && docker-compose down

docker_exec:
#	mkdir -p ${WORK_DIR}/docker/loki/.PythonFiles
	rm -rf ${WORK_DIR}/script/__pycache__ ${WORK_DIR}/script/.pytest_cache ${WORK_DIR}/script/.venv
#	cp -r ${WORK_DIR}/script ${MOUNT_VOLUME}
	cd ${WORK_DIR}/script && docker build ./ -t python_app
	cd ${WORK_DIR}/script && docker run -v /tmp/movies_data:/tmp -u root -it python_app /bin/bash /run.sh
	echo " <<<<---- 😃 Click this link ${LOKI_URL} to go to application logs and results links 😃 ---->>>>"

clean:
	.venv/bin/python ./main/json_format_push_to_mysql.py --db='presentation_db'

destroy: test
	.venv/bin/python ./main/json_format_push_to_mysql.py
