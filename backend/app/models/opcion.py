from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

class Opcion(SQLModel, table=True):
    __tablename__ = "opcion"
    id: int | None = Field(default=None, primary_key=True)
    grupo_id: int = Field(foreign_key="grupo_opcion.id", ondelete="CASCADE", index=True)
    valor: str = Field(max_length=100, nullable=False)
    codigo_hex: str | None = Field(default=None, max_length=7)
    modificador_precio: float = Field(default=0.0)
    orden: int = Field(default=0)
    grupo: Optional["GrupoOpcion"] = Relationship(back_populates="opciones")
    imagenes: list["OpcionImagen"] = Relationship(back_populates="opcion", sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"})
