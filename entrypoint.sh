#!/bin/sh

set -e

echo "Running migrations..."
poetry run alembic upgrade head

echo "Adding user admin..."
poetry run python src/scripts/add_user_admin.py

echo "Starting FastAPI app..."
exec poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload