from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class OpcionRead(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")
    valor: str
    codigo_hex: str | None = Field(default=None, alias="codigoHex")
    imagenes: list[str] = []
    modificador_precio: float = Field(default=0.0, alias="modificadorPrecio")

    @classmethod
    def from_opcion(cls, opcion):
        return cls(_id=str(opcion.id), valor=opcion.valor, codigoHex=opcion.codigo_hex,
                   imagenes=[img.imagen for img in (opcion.imagenes or [])], modificadorPrecio=opcion.modificador_precio)

class GrupoOpcionRead(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")
    tipo: str
    nombre: str
    opciones: list[OpcionRead] = []

    @classmethod
    def from_grupo(cls, grupo):
        return cls(_id=str(grupo.id), tipo=grupo.tipo, nombre=grupo.nombre,
                   opciones=[OpcionRead.from_opcion(op) for op in (grupo.opciones or [])])

class CategoriaNestedRead(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")
    nombre: str
    slug: str
    orden: int = 0
    icono: str | None = None
    created_at: datetime = Field(alias="createdAt")

    @classmethod
    def from_categoria(cls, cat):
        if cat is None: return None
        return cls(_id=str(cat.id), nombre=cat.nombre, slug=cat.slug, orden=cat.orden, icono=cat.icono, createdAt=cat.created_at)

class ProductoRead(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")
    nombre: str
    descripcion: str = ""
    categoria: CategoriaNestedRead | None = None
    precio_base: float = Field(alias="precioBase")
    imagenes_default: list[str] = Field(default=[], alias="imagenesDefault")
    grupos_opciones: list[GrupoOpcionRead] = Field(default=[], alias="gruposOpciones")
    activo: bool = True
    orden: int = 0
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime | None = Field(default=None, alias="updatedAt")

    @classmethod
    def from_producto(cls, prod):
        return cls(_id=str(prod.id), nombre=prod.nombre, descripcion=prod.descripcion or "",
                   categoria=CategoriaNestedRead.from_categoria(prod.categoria) if prod.categoria else None,
                   precioBase=prod.precio_base,
                   imagenesDefault=[img.imagen for img in (prod.imagenes_default or [])],
                   gruposOpciones=[GrupoOpcionRead.from_grupo(g) for g in (prod.grupos_opciones or [])],
                   activo=prod.activo if prod.activo is not None else True, orden=prod.orden or 0,
                   createdAt=prod.created_at, updatedAt=prod.updated_at)

class ProductoReadCart(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")
    nombre: str
    descripcion: str = ""
    categoria: str | None = None
    precio_base: float = Field(alias="precioBase")
    imagenes_default: list[str] = Field(default=[], alias="imagenesDefault")
    grupos_opciones: list[GrupoOpcionRead] = Field(default=[], alias="gruposOpciones")
    activo: bool = True
    orden: int = 0
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime | None = Field(default=None, alias="updatedAt")

    @classmethod
    def from_producto(cls, prod):
        return cls(_id=str(prod.id), nombre=prod.nombre, descripcion=prod.descripcion or "",
                   categoria=str(prod.categoria_id) if prod.categoria_id else None,
                   precioBase=prod.precio_base,
                   imagenesDefault=[img.imagen for img in (prod.imagenes_default or [])],
                   gruposOpciones=[GrupoOpcionRead.from_grupo(g) for g in (prod.grupos_opciones or [])],
                   activo=prod.activo if prod.activo is not None else True, orden=prod.orden or 0,
                   createdAt=prod.created_at, updatedAt=prod.updated_at)

class ProductoCreate(BaseModel):
    nombre: str
    descripcion: str = ""
    categoria: str = ""
    precioBase: float = 0.0
    orden: int = 0

class ProductoUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    categoria: str | None = None
    precioBase: float | None = None
    activo: bool | None = None
    orden: int | None = None

class ProductoReorder(BaseModel):
    ids: list[str]

class ImagenesReorder(BaseModel):
    imagenes: list[str]

class GrupoCreate(BaseModel):
    tipo: str
    nombre: str

class GrupoUpdate(BaseModel):
    nombre: str | None = None
    tipo: str | None = None

class OpcionReorder(BaseModel):
    opcionIds: list[str]

class OpcionUpdate(BaseModel):
    valor: str | None = None
    codigoHex: str | None = None
    modificadorPrecio: float | None = None
