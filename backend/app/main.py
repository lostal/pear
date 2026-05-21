from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.core.database import create_tables
from app.routers import auth, cart, categorias, productos, sitemap, users

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(title="Pear Backend", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=settings.UPLOADS_DIR), name="uploads")

api_prefix = "/api"
app.include_router(auth.router, prefix=api_prefix, tags=["auth"])
app.include_router(categorias.router, prefix=f"{api_prefix}/categorias", tags=["categorias"])
app.include_router(productos.router, prefix=f"{api_prefix}/productos", tags=["productos"])
app.include_router(cart.router, prefix=f"{api_prefix}/cart", tags=["cart"])
app.include_router(users.router, prefix=f"{api_prefix}/users", tags=["users"])
app.include_router(sitemap.router, prefix=api_prefix, tags=["sitemap"])

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"error": str(exc)})

@app.exception_handler(PermissionError)
async def permission_error_handler(request: Request, exc: PermissionError):
    return JSONResponse(status_code=403, content={"error": str(exc)})

@app.exception_handler(SQLAlchemyError)
async def db_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(status_code=500, content={"error": "Error en la base de datos"})
