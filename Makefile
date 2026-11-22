.PHONY: install test lint migrate api up down logs

install:
	python -m pip install -e ".[dev]"

test:
	pytest -q

lint:
	ruff check app tests scripts

migrate:
	python -m scripts.migrate

api:
	uvicorn app.main:app --reload

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f
