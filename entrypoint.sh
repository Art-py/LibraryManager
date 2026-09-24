#!/bin/sh

set -e

echo "Running migrations..."
uv run --no-sync alembic upgrade head

echo "Adding user admin..."
uv run --no-sync python -m src.presentation.cli.provision_admin

echo "Starting FastAPI app..."
exec uv run --no-sync uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
