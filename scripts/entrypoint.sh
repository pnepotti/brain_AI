#!/bin/bash
set -e

if [ -z "$1" ]; then
  set -- uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
fi

if [ "$1" = "uvicorn" ]; then
  echo "▶ Waiting for PostgreSQL..."
  while ! pg_isready -h $POSTGRES_SERVER -U $POSTGRES_USER -d $POSTGRES_DB; do
    sleep 1
  done

  echo "▶ Running migrations..."
  alembic upgrade head

  echo "▶ Initializing database with seed data..."
  python -m scripts.init_db
fi

echo "▶ Executing command: $@"
exec "$@"
