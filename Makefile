DC_COMP := docker-compose
SERVICE := backend

.PHONY: list
list: ## Показать список всех команд
	@echo "Доступные команды:"
	@echo
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: build
build:  ## Билд проекта
	$(DC_COMP) build --no-cache

.PHONY: up
up:  ## Запустить проект в контейнере докера
	$(DC_COMP) up -d

.PHONY: stop
stop:  ## Остановить контейнеры докера
	$(DC_COMP) stop

.PHONY: down
down:  ## Удалить контейнеры
	$(DC_COMP) down -v

.PHONY: format
format: ## Форматирование кода
	ruff format .
	ruff check . --select I --fix

.PHONY: linter
linter: ## Проверка стиля и удаление неиспользуемых импортов
	ruff check . --fix

.PHONY: test
test: ## Запуск тестов
	pytest -W 'ignore' -s test/

.PHONY: check-code
check-code:  ## полная проверка кода, формат, линтер и тесты
	ruff format .
	ruff check . --select I --fix
	ruff check . --fix
	pytest -W 'ignore' -s test/

.PHONY: migrations
migrations: ## Создание новой миграции: make migrations m="description"
	$(DC_COMP) exec $(SERVICE) poetry run alembic revision --autogenerate -m "$(m)"

.PHONY: migrate
migrate: ## Применение всех миграций
	$(DC_COMP) exec $(SERVICE) poetry run alembic upgrade head

.PHONY: downgrade
downgrade: ## Откат последней миграции
	$(DC_COMP) exec $(SERVICE) poetry run alembic downgrade -1
