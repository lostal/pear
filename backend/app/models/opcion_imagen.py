from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

class OpcionImagen(SQLModel, table=True):
    __tablename__ = "opcion_imagen"
    id: int | None = Field(default=None, primary_key=True)
    opcion_id: int = Field(foreign_key="opcion.id", ondelete="CASCADE", index=True)
    imagen: str = Field(max_length=500, nullable=False)
    orden: int = Field(default=0)
    opcion: Optional["Opcion"] = Relationship(back_populates="imagenes")
