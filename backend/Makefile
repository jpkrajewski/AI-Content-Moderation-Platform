# Variables
DB_URI=postgresql+psycopg2://jakub:secret@127.0.0.1:5432/moderation_db


migration:
	@echo "Running Alembic autogenerate with DB_URI=$(DB_URI)"
	@DB_URI=$(DB_URI) alembic revision --autogenerate -m "$(message)"

migrate:
	@DB_URI=$(DB_URI) alembic upgrade head


run_all_tests:
	@pytest

makemigrations:
	@alembic revision --autogenerate -m "$(message)"
