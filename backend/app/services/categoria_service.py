from sqlmodel import Session
from app.models.categoria import Categoria
from app.models.producto import Producto
from app.repositories.categoria_repo import CategoriaRepository

class CategoriaService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = CategoriaRepository(session)

    def get_all(self) -> list[Categoria]:
        return self.repo.get_all_ordered()

    def create(self, nombre: str, slug: str, orden: int = 0, icono: str | None = None) -> Categoria:
        existing = self.repo.get_by_slug(slug)
        if existing: raise ValueError("Slug ya existe")
        return self.repo.create(Categoria(nombre=nombre, slug=slug, orden=orden, icono=icono))

    def update(self, id_val: int, **data) -> Categoria:
        cat = self.repo.update_by_id(id_val, data)
        if not cat: raise ValueError("Categoría no encontrada")
        return cat

    def reorder(self, ids: list[str]) -> None:
        self.repo.reorder(ids)

    def delete(self, id_val: int) -> None:
        cat = self.repo.get_by_id(id_val)
        if not cat: raise ValueError("Categoría no encontrada")
        count = self.session.query(Producto).where(Producto.categoria_id == id_val).count()
        if count > 0: raise PermissionError("No se puede eliminar: hay productos en esta categoría")
        self.repo.delete(cat)
