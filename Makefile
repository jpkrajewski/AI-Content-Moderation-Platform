restart:
	@docker compose down -v
	@docker compose up -d
	@docker exec moderation-backend python /app/scripts/on_start/load_fixtures.py
	@docker exec moderation-backend python /app/scripts/on_start/load_clients_to_redis.py
	@echo "Database initialized and fixtures loaded."
	@echo "Load as Admin: admin_user:admin1234"
	@echo "Start frontedend"
	@npm --prefix ui run dev
