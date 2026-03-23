# Pear

SPA de gestión de productos e-commerce construida con **Svelte 5** en el frontend y **Express + MongoDB** en el backend. Incluye autenticación JWT, panel de administración con CRUD completo y gestión de usuarios por roles.

## Stack

| Capa | Tecnologías |
|---|---|
| Frontend | Svelte 5, Vite, TypeScript, Tailwind CSS 4 |
| Backend | Node.js, Express 4, MongoDB 6, Mongoose, Redis |
| Auth | JWT (Bearer token) |
| Infraestructura | Docker, Docker Compose |

---

## Inicio rápido

### Con Docker (recomendado)

```bash
docker compose up
```

Levanta MongoDB, Redis y el backend automáticamente. Luego inicia el frontend por separado:

```bash
cd frontend
pnpm install
pnpm dev
```

| Servicio | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend / API | http://localhost:3000 |
| Swagger UI | http://localhost:3000/api-docs |

### Desarrollo local (sin Docker)

**Backend:**

```bash
cd backend
pnpm install
cp .env.example .env   # ajusta las variables
pnpm dev
```

**Frontend:**

```bash
cd frontend
pnpm install
pnpm dev
```

> El frontend hace proxy de `/api` y `/uploads` al backend en `localhost:3000` (configurado en `vite.config.ts`).

### Variables de entorno

Copia `backend/.env.example` a `backend/.env` y ajusta:

```
MONGO_URI=mongodb://localhost:27017/pear
JWT_SECRET=tu_secreto
REDIS_URL=redis://localhost:6379
PORT=3000
```

### Datos de prueba

```bash
cd backend
pnpm seed
```

---

## Runas de Svelte 5 utilizadas

| Runa | Archivo(s) | Uso |
|---|---|---|
| `$state()` | `stores/auth.svelte.ts` | Token JWT y datos del usuario autenticado |
| `$state()` | `stores/products.svelte.ts` | Lista de productos y estado de carga |
| `$state()` | `stores/categories.svelte.ts` | Categorías disponibles |
| `$state()` | `stores/toast.svelte.ts` | Cola de notificaciones toast |
| `$state()` | `lib/ui.svelte.ts` | Estado de la UI (búsqueda abierta/cerrada) |
| `$derived()` | `stores/auth.svelte.ts` | `isAuthenticated`, `isAdmin`, `displayName` |
| `$derived()` | `stores/products.svelte.ts` | `byCategory` — productos agrupados y ordenados por categoría |
| `$effect()` | `App.svelte` | Protección de rutas: redirige al login si no hay sesión; actualiza el título de la pestaña |
| `$effect()` | `pages/LoginPage.svelte` | Redirige al catálogo si ya hay sesión activa |
| `$effect()` | `pages/AdminUsersPage.svelte` | Carga usuarios cuando el rol admin está confirmado |
| `$props()` | `components/products/*`, `components/ui/*` | Props y callbacks en `ProductCard`, `ProductForm`, `UserRow`, `Modal`, `Button`, `Input`, etc. |

Los callbacks (`onSave`, `onDelete`, `onEdit`) sustituyen a los eventos personalizados clásicos para la comunicación hijo → padre.

---

## API consumida

| Método | Endpoint | Rol | Descripción |
|---|---|---|---|
| `POST` | `/api/auth/login` | Público | Login, devuelve JWT |
| `GET` | `/api/products` | Autenticado | Listar productos |
| `POST` | `/api/products` | Admin | Crear producto |
| `PUT` | `/api/products/:id` | Admin | Editar producto |
| `DELETE` | `/api/products/:id` | Admin | Eliminar producto |
| `GET` | `/api/categories` | Autenticado | Listar categorías |
| `GET` | `/api/users` | Admin | Listar usuarios |
| `PUT` | `/api/users/:id` | Admin | Editar usuario / cambiar rol |
| `DELETE` | `/api/users/:id` | Admin | Eliminar usuario |

La documentación completa de la API está disponible en Swagger: `http://localhost:3000/api-docs`

---

## Funcionalidades

- **Autenticación JWT** con persistencia en `localStorage` y restauración de sesión al recargar
- **Catálogo de productos** agrupado por categorías con búsqueda y filtros
- **Panel de administración** — CRUD completo de productos y usuarios (solo rol `admin`)
- **Gestión de roles** — acciones visibles según rol del usuario autenticado
- **Detalle de producto** con opciones de color, almacenamiento y precio
- **Notificaciones toast** para feedback de acciones
- **Skeletons y spinners** durante la carga de datos
- **Confirmación** en acciones destructivas (borrar producto/usuario)
- **Tema claro/oscuro** con sistema de variables CSS
- **Diseño responsive** con Tailwind CSS
