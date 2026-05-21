from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

class ProductoImagenDefault(SQLModel, table=True):
    __tablename__ = "producto_imagen_default"
    id: int | None = Field(default=None, primary_key=True)
    producto_id: int = Field(foreign_key="producto.id", ondelete="CASCADE", index=True)
    imagen: str = Field(max_length=500, nullable=False)
    orden: int = Field(default=0)
    producto: Optional["Producto"] = Relationship(back_populates="imagenes_default")
