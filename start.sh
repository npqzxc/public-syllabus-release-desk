#!/bin/sh

set -eu

if [ ! -d /app/.git ]; then
    echo "Expected git repository at /app" >&2
    exit 1
fi

mkdir -p /app/data

export DATABASE_URL="${DATABASE_URL:-postgresql+psycopg://coursestudio:coursestudio@127.0.0.1:5432/coursestudio}"
export VENDOR_HUB_HOST="${VENDOR_HUB_HOST:-0.0.0.0}"
export VENDOR_HUB_PORT="${VENDOR_HUB_PORT:-8000}"

service postgresql start >/dev/null 2>&1 || pg_ctlcluster 15 main start >/dev/null 2>&1 || true

su postgres -c "psql -tAc \"SELECT 1 FROM pg_roles WHERE rolname='coursestudio'\" | grep -q 1 || psql -c \"CREATE ROLE coursestudio LOGIN PASSWORD 'coursestudio';\""
su postgres -c "psql -tAc \"SELECT 1 FROM pg_database WHERE datname='coursestudio'\" | grep -q 1 || psql -c \"CREATE DATABASE coursestudio OWNER coursestudio;\""

python3 - <<'PY'
from app.config import build_settings
from app.db import init_db, reset_engine
from app.seed import ensure_seed_data

settings = build_settings()
reset_engine(settings.database_url)
init_db()
if settings.seed_data:
    ensure_seed_data()
print("Course Studio database warmed")
PY

exec python3 -m app.server
