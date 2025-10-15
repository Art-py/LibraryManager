.PHONY: list
list: ## Показать список всех команд
	@echo "Доступные команды:"
	@echo
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: start-dev
start-dev: ## Запуск сервиса в режиме разработки (с авто-перезагрузкой)
	uvicorn src.main:app --reload

.PHONY: format
format: ## Форматирование кода
	ruff format .
	ruff check . --select I --fix

.PHONY: linter
linter: ## Проверка стиля и удаление неиспользуемых импортов
	ruff check . --fix

.PHONY: test
test: ## Запуск тестов
	pytest -s test/

.PHONY: migrate
migrate: ## Создание новой миграции: make migrate m="description"
	poetry run alembic revision --autogenerate -m "$(m)"

.PHONY: upgrade
upgrade: ## Применение всех миграций
	poetry run alembic upgrade head

.PHONY: downgrade
downgrade: ## Откат последней миграции
	poetry run alembic downgrade -1
