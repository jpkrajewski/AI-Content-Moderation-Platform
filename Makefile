.PHONY: stop start rebuild restart load_fixtures

stop:
	docker compose down
	npm --prefix ui run stop

start:
	docker compose up -d
	npm --prefix ui run dev

rebuild:
	docker compose down -v
	docker compose up --build -d

reset: rebuild load_fixtures download_ai_models start

load_fixtures:
	docker compose down backend
	docker compose up backend -d
	docker compose exec -T backend python /app/src/moderation/scripts/load_fixtures.py

download_ai_models:
	docker compose exec -T backend python /app/src/moderation/scripts/download_ai_models.py
