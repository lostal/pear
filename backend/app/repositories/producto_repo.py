from sqlmodel import Session, select
from app.models.producto import Producto
from app.models.categoria import Categoria
from app.repositories.base import BaseRepository

class ProductoRepository(BaseRepository[Producto]):
    def __init__(self, session: Session):
        super().__init__(Producto, session)

    def get_all_active(self, categoria_slug: str | None = None) -> list[Producto]:
        stmt = select(Producto).where(Producto.activo == True).order_by(Producto.orden)
        if categoria_slug:
            stmt = stmt.join(Categoria).where(Categoria.slug == categoria_slug)
        return list(self.session.exec(stmt).all())

    def get_by_id_with_relations(self, id_val: int) -> Producto | None:
        return self.session.get(Producto, id_val)

    def update_by_id(self, id_val: int, data: dict) -> Producto | None:
        prod = self.session.get(Producto, id_val)
        if not prod: return None
        if "id" in data: del data["id"]
        for key, value in data.items():
            if value is not None: setattr(prod, key, value)
        self.session.add(prod)
        self.session.commit()
        self.session.refresh(prod)
        return prod

    def reorder(self, ids: list[str]) -> None:
        for index, id_str in enumerate(ids):
            prod = self.session.get(Producto, int(id_str))
            if prod:
                prod.orden = index
                self.session.add(prod)
        self.session.commit()

    def delete_by_id(self, id_val: int) -> bool:
        prod = self.session.get(Producto, id_val)
        if not prod: return False
        self.session.delete(prod)
        self.session.commit()
        return True
