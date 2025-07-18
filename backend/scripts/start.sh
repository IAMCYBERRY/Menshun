#!/bin/bash
set -e

echo "🚀 Starting Menshun PAM Backend..."
echo "Environment: ${ENVIRONMENT:-development}"
echo "Build Date: ${BUILD_DATE:-unknown}"
echo "VCS Ref: ${VCS_REF:-unknown}"

# Wait for database
echo "⏳ Waiting for database connection..."
python scripts/wait_for_db.py

# Run database migrations
echo "📈 Running database migrations..."
alembic upgrade head

# Seed directory roles if needed
echo "🌱 Seeding directory roles..."
python -m app.scripts.seed_roles --if-empty || python -m app.scripts.seed_roles

# Start the application
echo "🎯 Starting FastAPI server..."
exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers ${WORKERS:-1} \
    --log-level ${LOG_LEVEL:-info} \
    --access-log \
    --reload