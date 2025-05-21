# Variables
DB_URI=postgresql+psycopg2://jakub:secret@127.0.0.1:5432/moderation_db

# Default target for creating a migration
migration:
	@echo "Running Alembic autogenerate with DB_URI=$(DB_URI)"
	@DB_URI=$(DB_URI) alembic revision --autogenerate -m "$(message)"

# Target to create and apply migration
migrate:
	@echo "Running Alembic upgrading DB with DB_URI=$(DB_URI)"
	@DB_URI=$(DB_URI) alembic upgrade head

# Help target to display usage
help:
	@echo "Available commands:"
	@echo "  make migration message=\"<migration message>\"  - Run alembic revision with autogenerate"
	@echo "  make migrate  - Run alembic upgrade database"


run_all_tests:
	@echo "Running all unit tests"
	@pytest

makemigrations:
	@alembic revision --autogenerate -m "$(message)"

migrate:
	@alembic upgrade head
