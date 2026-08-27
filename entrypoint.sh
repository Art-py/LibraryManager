#!/bin/sh

set -e

echo "Running migrations..."
uv run --no-sync alembic upgrade head

echo "Adding user admin..."
uv run --no-sync python src/scripts/add_user_admin.py

echo "Starting FastAPI app..."
exec uv run --no-sync uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
