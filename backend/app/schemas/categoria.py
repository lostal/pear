from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class CategoriaRead(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")
    nombre: str
    slug: str
    orden: int = 0
    icono: str | None = None
    created_at: datetime = Field(alias="createdAt")

class CategoriaCreate(BaseModel):
    nombre: str
    slug: str
    orden: int = 0
    icono: str | None = None

class CategoriaUpdate(BaseModel):
    nombre: str | None = None
    slug: str | None = None
    orden: int | None = None
    icono: str | None = None

class CategoriaReorder(BaseModel):
    ids: list[int | str]
