.PHONY: stop start rebuild restart load_fixtures

stop:
	docker compose down
	npm --prefix ui run stop

start:
	docker compose up -d
	npm --prefix ui run dev
	@echo "✅ Frontend started at http://localhost:3000"

rebuild:
	docker compose down -v
	docker compose up --build -d

restart: rebuild start load_fixtures

load_fixtures:
	docker compose exec -T backend python /app/src/moderation/scripts/load_fixtures.py
