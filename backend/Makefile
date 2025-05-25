# Variables
DB_URI=postgresql+psycopg2://jakub:secret@127.0.0.1:5432/moderation_db


migration:
	@echo "Running Alembic autogenerate with DB_URI=$(DB_URI)"
	@DB_URI=$(DB_URI) alembic revision --autogenerate -m "$(message)"

migrate:
	@DB_URI=$(DB_URI) alembic upgrade head


run_test_db:
	docker run -d \
		-e POSTGRES_USER=test_postgres \
		-e POSTGRES_PASSWORD=password \
		--name test_postgres -p 5433:5432 --rm postgres:11-alpine

clean_test_db:
	docker rm -f -v test_postgres


run_all_tests: clean_test_db run_test_db
	pytest -v -s

makemigrations:
	@alembic revision --autogenerate -m "$(message)"
