#!/bin/bash
set -e

cd /var/www/pear

echo "=== Pulling latest changes ==="
git pull

echo "=== Building frontend ==="
cd frontend
pnpm install --frozen-lockfile
pnpm build
cd ..

echo "=== Rebuilding and restarting containers ==="
docker compose -f docker-compose.prod.yml up -d --build --remove-orphans

echo "=== Cleaning up old images ==="
docker image prune -f

echo "=== Done ==="
