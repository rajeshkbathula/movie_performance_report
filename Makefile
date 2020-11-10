RUN: test_script docker_up script_exec
STOP: docker_down clean

WORK_DIR=$(shell pwd)
PYTHON       ?=python # change here how you set bash profile your python like python3 or python
PIP_VERSION  ?=PIP # PIP or PIP3
DATA_PATH    ?=$(WORK_DIR)/script/data  #absolut path to raw files folder and no changes to names expected
GRAFANA_URL     ?=http://localhost:9000/explore?orgId=1&left=%5B%22now-1h%22,%22now%22,%22loki%22,%7B%22expr%22:%22%7Bmovie_database%3D%5C%22top_revenue_movies%5C%22%7D%22%7D%5D

docker_up:
	cd ./docker && docker-compose up -d

test_script:
	cd script && virtualenv ./.venv; \
	source ./.venv/bin/activate;  $(PIP_VERSION) install -r  requirements.txt; \
	pytest ./test/test_main_script.py

script_exec:
	cd script && source ./.venv/bin/activate;  $(PIP_VERSION) install -r  requirements.txt; \
	pytest ./test/ ; \
	echo " <<<<---- 😃 Click this link ${GRAFANA_URL} to go to application logs and results links 😃 ---->>>>"; \
	$(PYTHON) main.py --input_location=$(DATA_PATH)
	echo "Successfully Created View!"

docker_down:
	cd ${WORK_DIR}/docker && docker-compose down

clean:
	rm -rf ./script/.evnv ./script/.pytest_cache ./script/__pytest_cache__
