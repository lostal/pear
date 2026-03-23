# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Use **pnpm** (not npm or yarn).

### Frontend (`/frontend`)
```bash
pnpm dev        # Dev server (proxies /api and /uploads to backend:3000)
pnpm build      # TypeScript check + Vite build
pnpm lint       # ESLint
pnpm format     # Prettier
```

### Backend (`/backend`)
```bash
pnpm dev        # Nodemon dev server
pnpm start      # Production
pnpm seed       # Seed database
pnpm test       # Jest (runs --runInBand, sequential)
pnpm lint       # ESLint
pnpm format     # Prettier
```

### Infrastructure
```bash
docker-compose up   # Starts MongoDB, Redis, and backend (with auto-seed)
```

Requires a `/backend/.env` file — copy from `.env.example`. Minimum: `MONGO_URI`, `JWT_SECRET`.

API docs available at `http://localhost:3000/api-docs` (Swagger UI).

## Architecture

Full-stack SPA with a Svelte 5 frontend and Express.js backend. No monorepo tooling — each side has its own `package.json`.

### Frontend (`/frontend/src`)

- **Routing**: Custom client-side router (`lib/Router.svelte` + `lib/router.svelte.ts`) with lazy-loaded page components and route caching (`lib/routeCache.ts`). Route protection runs via `$effect()` in `App.svelte`.
- **State**: Svelte 5 Runes (`$state`, `$derived`, `$effect`, `$props`) — no legacy stores. State modules live in `stores/*.svelte.ts`.
- **API layer**: `services/http.ts` is a fetch wrapper that injects the JWT token. All other services (`auth.service.ts`, `products.service.ts`, `users.service.ts`) call through it.
- **Types**: Shared TypeScript interfaces (User, Product, Category, etc.) in `types/index.ts`.
- **Styles**: Tailwind CSS 4 via `@tailwindcss/vite` plugin. Global styles in `app.css`. Fonts: IBM Plex Sans + Instrument Serif.

### Backend (`/backend/src`)

- **Pattern**: MVC with a service layer — routes → controllers → services → Mongoose models.
- **Auth**: JWT Bearer tokens. `middleware/authMiddleware.js` verifies tokens and injects `req.user`. Role-based access control (admin/user) enforced per-route.
- **Models**: `User` (with embedded cart), `Producto` (complex option groups: color with images, storage with price modifiers), `Categoria`.
- **Caching**: Redis client configured in `config/redis.js`.
- **File uploads**: Multer stores product images in `/backend/uploads/`, served as static files.
- **Rate limiting**: `middleware/rateLimiter.js` via `express-rate-limit`.

### Data flow for product options
Products have option groups where each color variant carries its own images and each storage variant has a price delta. The frontend components (`ColorSwatch.svelte`, `StorageSelector.svelte`) reflect this structure directly.
