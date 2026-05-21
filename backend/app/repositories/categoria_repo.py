from sqlmodel import Session, select
from app.models.categoria import Categoria
from app.repositories.base import BaseRepository

class CategoriaRepository(BaseRepository[Categoria]):
    def __init__(self, session: Session):
        super().__init__(Categoria, session)

    def get_all_ordered(self) -> list[Categoria]:
        return list(self.session.exec(select(Categoria).order_by(Categoria.orden)).all())

    def get_by_slug(self, slug: str) -> Categoria | None:
        return self.session.exec(select(Categoria).where(Categoria.slug == slug)).first()

    def update_by_id(self, id_val: int, data: dict) -> Categoria | None:
        cat = self.session.get(Categoria, id_val)
        if not cat: return None
        for key, value in data.items():
            if value is not None: setattr(cat, key, value)
        self.session.add(cat)
        self.session.commit()
        self.session.refresh(cat)
        return cat

    def reorder(self, ids: list[str]) -> None:
        for index, id_str in enumerate(ids):
            cat = self.session.get(Categoria, int(id_str))
            if cat:
                cat.orden = index
                self.session.add(cat)
        self.session.commit()
