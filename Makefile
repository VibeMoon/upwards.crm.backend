PROJECT_NAME := vibemoon

DOCKER_COMPOSE := docker-compose.yml

WEB_SERVICE := web
DB_SERVICE := db

ENV_FILE := .env.prod

.PHONY: help build up down logs migrate createsuperuser shell test

help:
	@echo "Использование:"
	@echo "  make build            - Собрать Docker образы"
	@echo "  make up               - Запустить все контейнеры"
	@echo "  make down             - Остановить все контейнеры"
	@echo "  make logs             - Показать логи всех контейнеров"
	@echo "  make migrate          - Выполнить миграции базы данных"
	@echo "  make createsuperuser  - Создать суперпользователя"
	@echo "  make shell            - Открыть Django shell"
	@echo "  make test             - Запустить тесты"

build:
	docker-compose -f $(DOCKER_COMPOSE) build

up:
	docker-compose -f $(DOCKER_COMPOSE) up -d

down:
	docker-compose -f $(DOCKER_COMPOSE) down

logs:
	docker-compose -f $(DOCKER_COMPOSE) logs -f

createsuperuser:
	docker-compose -f $(DOCKER_COMPOSE) exec $(WEB_SERVICE) python app/manage.py createsuperuser

shell:
	docker-compose -f $(DOCKER_COMPOSE) exec $(WEB_SERVICE) python app/manage.py shell

test:
	docker-compose -f $(DOCKER_COMPOSE) exec $(WEB_SERVICE) python app/manage.py test

run:
	docker-compose -f $(DOCKER_COMPOSE) exec $(WEB_SERVICE) python app/manage.py collectstatic --noinput
	docker-compose -f $(DOCKER_COMPOSE) exec $(WEB_SERVICE) python app/manage.py migrate
	docker-compose -f $(DOCKER_COMPOSE) exec $(WEB_SERVICE) python -m gunicorn --bind 0.0.0.0:8000 --workers 3 config.wsgi:application
