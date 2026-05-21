# AGENTS.md

## Commands

### Frontend (`/frontend`)
```bash
pnpm dev         # Dev server, proxies /api and /uploads → localhost:3001
pnpm build       # tsc (typecheck) + vite build
pnpm lint        # ESLint
pnpm format      # Prettier (singleQuote, printWidth 100, trailingComma es5)
```

### Backend (`/backend`) — Python 3.13+ / FastAPI
```bash
uv sync                                  # Install deps
uv run python seed.py                    # Seed DB (admin/admin123, user/user123)
uv run uvicorn app.main:app --port 3001 --reload
uv run python -m pytest -v               # Run all tests
```

**Env**: backend needs `DATABASE_URL`, `JWT_SECRET`, and optionally `JWT_EXPIRE_MINUTES`. Copy `backend/.env` from the example does **not** match the real config — the actual env file has different keys than `.env.example`.

## Architecture

### Backend: Router → Service → Repository

Each layer calls only the one below. Routers are thin; business logic lives in services; data access in repositories (generic `BaseRepository[T]`).

Pydantic schemas use **camelCase** field aliases (`precioBase`, `imagenesDefault`) so the JSON API matches the frontend's expected keys. Always use `populate_by_name=True` on read schemas.

**Critical import**: The `create_tables()` function in `core/database.py` does `import app.models` to discover all SQLModel tables. The `app/models/__init__.py` must import every model class or tables won't be created. When adding a new model, add its import there.

**SQLite quirks**:
- Foreign keys are enabled per-connection via a SQLAlchemy `connect` event listener (`PRAGMA foreign_keys=ON`).
- `connect_args={"check_same_thread": False}` is set on the engine.

**Auth**: JWT Bearer. `dependencies.py` provides `get_current_user` (extracts user from token) and `require_admin` (403 if role != "admin"). In-memory rate limiter on login (5 attempts / 15 min).

**Tests** run against the real SQLite database. Tests reset the rate limiter state with `rate_limiter.attempts = {}` before login calls to avoid 429s.

### Frontend: Svelte 5 SPA

- Custom client-side router (`lib/router.svelte.ts`): uses `history.replaceState` + `history.pushState` to preserve scroll position during navigation.
- Routes defined in `App.svelte` with lazy `import()`.
- `services/http.ts`: fetch wrapper that auto-injects JWT from the auth store, sets `Content-Type: application/json` (except for FormData uploads — use `http.postForm`), and handles 401/403 by logging out.
- Tailwind CSS 4 via `@tailwindcss/vite` plugin. No `tailwind.config` file.
- Stores are Svelte 5 `.svelte.ts` files using `$state` and `$derived` runes (not Svelte 4 stores).

### Data migration (legacy MongoDB → SQLite)
```bash
docker compose up -d mongo
cd backend && uv run python migrate.py
docker stop mongo
```
Only needed if migrating from the old Node.js/MongoDB backend. Not part of normal development workflow.
