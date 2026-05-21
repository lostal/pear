from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

class Categoria(SQLModel, table=True):
    __tablename__ = "categoria"
    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=150, nullable=False)
    slug: str = Field(max_length=150, unique=True, nullable=False, index=True)
    orden: int = Field(default=0)
    icono: str | None = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    productos: list["Producto"] = Relationship(back_populates="categoria", sa_relationship_kwargs={"lazy": "selectin"})
