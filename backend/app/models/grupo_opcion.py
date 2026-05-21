from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

class GrupoOpcion(SQLModel, table=True):
    __tablename__ = "grupo_opcion"
    id: int | None = Field(default=None, primary_key=True)
    producto_id: int = Field(foreign_key="producto.id", ondelete="CASCADE", index=True)
    tipo: str = Field(max_length=20, nullable=False)
    nombre: str = Field(max_length=100, nullable=False)
    orden: int = Field(default=0)
    producto: Optional["Producto"] = Relationship(back_populates="grupos_opciones")
    opciones: list["Opcion"] = Relationship(back_populates="grupo", sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"})
