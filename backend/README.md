# Pear Backend

Backend Python con FastAPI, SQLModel y SQLite. Reemplaza al antiguo backend Node.js/Express/MongoDB.

## Instalación

cd backend
uv sync
cp .env.example .env
uv run python seed.py     # crea admin/admin123 y user/user123

## Ejecución

uv run uvicorn app.main:app --port 3001 --reload

Swagger: http://localhost:3001/docs

## Tests

uv run python -m pytest -v

## Migración desde MongoDB

Requiere tener MongoDB corriendo con los datos antiguos.
uv run python migrate.py
