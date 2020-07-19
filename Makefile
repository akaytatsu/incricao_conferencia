SHELL:=/bin/bash
ARGS = $(filter-out $@,$(MAKECMDGOALS))
MAKEFLAGS += --silent
BASE_PATH=${PWD}
PYTHON_EXEC=python
DOCKER_COMPOSE_FILE=$(shell echo -f docker-compose.yml)

include .env
export $(shell sed 's/=.*//' .env)

show_env:
	# Show wich DOCKER_COMPOSE_FILE and ENV the recipes will user
	# It should be referenced by all other recipes you want it to show.
	# It's only printed once even when more than a recipe executed uses it
	sh -c "if [ \"${ENV_PRINTED:-0}\" != \"1\" ]; \
	then \
		echo DOCKER_COMPOSE_FILE = \"${DOCKER_COMPOSE_FILE}\"; \
		echo OSFLAG = \"${OSFLAG}\"; \
	fi; \
	ENV_PRINTED=1;"

_cp_env_file:
	cp -f .env.sample .env

init: show_env _cp_env_file

_build: show_env
	docker-compose ${DOCKER_COMPOSE_FILE} build

_rebuild: show_env
	docker-compose ${DOCKER_COMPOSE_FILE} down
	docker-compose ${DOCKER_COMPOSE_FILE} build --no-cache --force-rm

up: show_env
	docker-compose ${DOCKER_COMPOSE_FILE} up -d

flake8: show_env
	echo "verify pep8 ..."
	docker-compose ${DOCKER_COMPOSE_FILE} exec app flake8 . && isort . -rc

log: show_env
	docker-compose ${DOCKER_COMPOSE_FILE} logs -f app

stop: show_env
	docker-compose ${DOCKER_COMPOSE_FILE} stop

status: show_env
	docker-compose ${DOCKER_COMPOSE_FILE} ps

restart: show_env
	docker-compose ${DOCKER_COMPOSE_FILE} restart

sh: show_env
	docker-compose ${DOCKER_COMPOSE_FILE} exec ${ARGS} bash

test: show_env
	docker-compose ${DOCKER_COMPOSE_FILE} exec app pytest

psql: show_env
	docker-compose ${DOCKER_COMPOSE_FILE} exec db psql -d database

pgcli: show_env
	docker-compose ${DOCKER_COMPOSE_FILE} exec app pgcli postgres://${DB_USER}:${DB_PASS}@${DB_HOST}:${DB_PORT}/${DB_NAME}

_drop_db:
	docker-compose ${DOCKER_COMPOSE_FILE} stop db
	docker-compose ${DOCKER_COMPOSE_FILE} rm db

_create_db:
	docker-compose ${DOCKER_COMPOSE_FILE} up -d db

recreate_db: show_env _drop_db _create_db

createsuperuser: show_env
	docker-compose ${DOCKER_COMPOSE_FILE} exec app ${PYTHON_EXEC} ./manage.py shell -c "from apps.user.models import Usuario; Usuario.objects.create_superuser('root@root.com.br', 'root', name='root'); print('Superuser created: root@root.com.br:root')"

fixtures: show_env
	docker-compose ${DOCKER_COMPOSE_FILE} exec app pytest --fixtures

migrate: show_env
	docker-compose ${DOCKER_COMPOSE_FILE} exec app ${PYTHON_EXEC} manage.py migrate ${ARGS}

makemigrations: show_env
	docker-compose ${DOCKER_COMPOSE_FILE} exec app ${PYTHON_EXEC} manage.py makemigrations ${ARGS}
	docker-compose ${DOCKER_COMPOSE_FILE} exec app ${PYTHON_EXEC} manage.py migrate

pip_install: show_env
	docker-compose ${DOCKER_COMPOSE_FILE} exec app ${PYTHON_EXEC} -m pip install -r requirements.txt

manage: show_env
	docker-compose ${DOCKER_COMPOSE_FILE} exec app ${PYTHON_EXEC} manage.py ${ARGS}

test-watch: show_env
	docker-compose ${DOCKER_COMPOSE_FILE} exec app pytest --testmon "${ARGS}"

html: show_env
	docker-compose ${DOCKER_COMPOSE_FILE} exec app pytest --cov --cov-report xml:coverage.xml
	docker-compose ${DOCKER_COMPOSE_FILE} exec app coverage html

clean_db: show_env
	docker-compose ${DOCKER_COMPOSE_FILE} exec db psql -d ${DB_NAME} -c 'drop schema public cascade; create schema public;'