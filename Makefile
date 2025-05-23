stop:
	@docker compose down
	@echo "Containers stopped."
	@echo "Stop frontend"
	@npm --prefix ui run stop
	@echo "Frontend stopped."


start:
	@docker compose up -d
	@npm --prefix ui run dev
	@echo "Frontend started."


rebuild:
	@docker compose down -v
	@docker compose up --build -d

load_fixtures:
	@docker compose exec -T backend python /app/src/moderation/scripts/load_fixtures.py
