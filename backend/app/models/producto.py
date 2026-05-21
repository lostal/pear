from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

class Producto(SQLModel, table=True):
    __tablename__ = "producto"
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=200, nullable=False)
    descripcion: str = Field(default="", max_length=2000)
    categoria_id: int | None = Field(default=None, foreign_key="categoria.id", ondelete="SET NULL", index=True)
    precio_base: float = Field(nullable=False)
    activo: bool = Field(default=True)
    orden: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default=None)
    categoria: Optional["Categoria"] = Relationship(back_populates="productos")
    grupos_opciones: list["GrupoOpcion"] = Relationship(back_populates="producto", sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"})
    imagenes_default: list["ProductoImagenDefault"] = Relationship(back_populates="producto", sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"})
