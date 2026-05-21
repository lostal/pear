# Pear

![Hero](/frontend/src/assets/collage.png)

SPA de gestión de productos e-commerce construida con **Svelte 5** (frontend) y **FastAPI + SQLite** (backend Python). Incluye autenticación JWT, panel de administración con CRUD completo y gestión de usuarios por roles.

> Memoria de Uso de IA disponible en [docs/practica2-ia-prompts.md](docs/practica2-ia-prompts.md).

## Stack

| Capa            | Tecnologías                                |
| --------------- | ------------------------------------------ |
| Frontend        | Svelte 5, Vite, TypeScript, Tailwind CSS 4 |
| Backend         | Python, FastAPI, SQLModel, SQLite          |
| Auth            | JWT (Bearer token)                         |
| Infraestructura | Docker, Docker Compose (opcional)          |

---

## Inicio rápido

### Backend Python

```bash
cd backend
uv sync                 # Instalar dependencias
cp .env.example .env    # Configurar variables
uv run python seed.py   # Crear datos de prueba (admin/admin123)
uv run uvicorn app.main:app --port 3001 --reload   # Iniciar servidor
```
Swagger: http://localhost:3001/docs

### Frontend

```bash
cd frontend
pnpm install
pnpm dev
```

### Migrar datos desde el backend legacy

```bash
docker compose up -d mongo   # Iniciar MongoDB
cd backend && uv run python migrate.py  # Migrar datos a SQLite
docker stop mongo            # Parar MongoDB
```

### Servicios activos

| Servicio    | URL                           |
| ----------- | ----------------------------- |
| Frontend    | http://localhost:5173         |
| Backend API | http://localhost:3001         |
| Swagger UI  | http://localhost:3001/docs    |
| Uploads     | http://localhost:3001/uploads |

### Variables de entorno (`backend/.env`)

```
DATABASE_URL=sqlite:///./pear.db
JWT_SECRET=pear-jwt-secret-key-2026
JWT_EXPIRE_MINUTES=60
```

### Datos de prueba

```bash
cd backend
uv run python seed.py   # crea admin/admin123 y user/user123
```

---

## Diseño

Las maquetas de productos, logo e identidad visual del proyecto están elaboradas en Figma.

[![Figma Design Kit](https://img.shields.io/badge/Figma-Pear%20Design%20Kit-F24E1E?logo=figma&logoColor=white)](https://www.figma.com/design/LYq8hznI5C1nRtyJ7C7pzt/Pear-Design-Kit)

---

## Migración de datos (Node.js/MongoDB → Python/SQLite)

Para migrar los datos del backend legacy:

```bash
# 1. Levantar MongoDB con Docker
docker compose up -d mongo

# 2. Ejecutar migración
cd backend
uv run python migrate.py
```

Esto copia categorías, productos (con imágenes, grupos y opciones), usuarios y carritos al nuevo backend.

---

## Arquitectura del backend Python

```
backend/
├── app/
│   ├── main.py              # FastAPI app, CORS, static files
│   ├── dependencies.py      # get_db, get_current_user, require_admin
│   ├── core/
│   │   ├── config.py        # Settings (DATABASE_URL, JWT_SECRET)
│   │   ├── database.py      # SQLite engine + session
│   │   └── security.py      # JWT, password hashing (Argon2 + bcrypt)
│   ├── models/              # SQLModel tables (8 tablas)
│   ├── schemas/             # Pydantic request/response (API shapes)
│   ├── routers/             # HTTP handlers (6 routers)
│   ├── services/            # Lógica de negocio
│   └── repositories/        # Acceso a datos (patrón repositorio)
├── uploads/                 # Imágenes de productos
├── seed.py                  # Datos de prueba
├── migrate.py               # Migración MongoDB → SQLite
└── .env                     # Variables de entorno
```

## **Separación de responsabilidades:** Router → Service → Repository. Cada capa solo depende de la inmediatamente inferior. Los routers no contienen lógica de negocio ni acceso directo a base de datos.

## Runas de Svelte 5 utilizadas

| Runa         | Archivo(s)                                 | Uso                                                                                            |
| ------------ | ------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| `$state()`   | `stores/auth.svelte.ts`                    | Token JWT y datos del usuario autenticado                                                      |
| `$state()`   | `stores/products.svelte.ts`                | Lista de productos y estado de carga                                                           |
| `$state()`   | `stores/categories.svelte.ts`              | Categorías disponibles                                                                         |
| `$state()`   | `stores/toast.svelte.ts`                   | Cola de notificaciones toast                                                                   |
| `$state()`   | `lib/ui.svelte.ts`                         | Estado de la UI (búsqueda abierta/cerrada)                                                     |
| `$derived()` | `stores/auth.svelte.ts`                    | `isAuthenticated`, `isAdmin`, `displayName`                                                    |
| `$derived()` | `stores/products.svelte.ts`                | `byCategory` — productos agrupados y ordenados por categoría                                   |
| `$effect()`  | `App.svelte`                               | Protección de rutas: redirige al login si no hay sesión; actualiza el título de la pestaña     |
| `$effect()`  | `pages/LoginPage.svelte`                   | Redirige al catálogo si ya hay sesión activa                                                   |
| `$effect()`  | `pages/AdminUsersPage.svelte`              | Carga usuarios cuando el rol admin está confirmado                                             |
| `$props()`   | `components/products/*`, `components/ui/*` | Props y callbacks en `ProductCard`, `ProductForm`, `UserRow`, `Modal`, `Button`, `Input`, etc. |

Los callbacks (`onSave`, `onDelete`, `onEdit`) sustituyen a los eventos personalizados clásicos para la comunicación hijo → padre.

---

## API

| Método   | Endpoint               | Auth | Rol   | Descripción                  |
| -------- | ---------------------- | ---- | ----- | ---------------------------- |
| `POST`   | `/api/login`           | No   | -     | Login, devuelve JWT          |
| `POST`   | `/api/register`        | No   | -     | Registrar usuario            |
| `GET`    | `/api/productos`       | No   | -     | Listar productos activos     |
| `GET`    | `/api/productos/:id`   | No   | -     | Detalle de producto          |
| `POST`   | `/api/productos`       | JWT  | admin | Crear producto               |
| `PUT`    | `/api/productos/:id`   | JWT  | admin | Editar producto              |
| `DELETE` | `/api/productos/:id`   | JWT  | admin | Eliminar producto            |
| `GET`    | `/api/categorias`      | No   | -     | Listar categorías            |
| `POST`   | `/api/categorias`      | JWT  | admin | Crear categoría              |
| `PUT`    | `/api/categorias/:id`  | JWT  | admin | Editar categoría             |
| `DELETE` | `/api/categorias/:id`  | JWT  | admin | Eliminar categoría           |
| `GET`    | `/api/cart`            | JWT  | user  | Ver carrito                  |
| `POST`   | `/api/cart/add`        | JWT  | user  | Añadir al carrito            |
| `DELETE` | `/api/cart/:productId` | JWT  | user  | Eliminar del carrito         |
| `GET`    | `/api/users`           | JWT  | admin | Listar usuarios              |
| `PUT`    | `/api/users/:id`       | JWT  | admin | Editar usuario / cambiar rol |
| `DELETE` | `/api/users/:id`       | JWT  | admin | Eliminar usuario             |

Endpoints adicionales para gestión de grupos de opciones e imágenes en productos disponibles vía Swagger: `http://localhost:3001/docs`

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
