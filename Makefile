# Copyright (c) Dario Pizzolante
.PHONY: up down logs api db-upgrade

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

api:
	uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload

db-upgrade:
	alembic upgrade head
