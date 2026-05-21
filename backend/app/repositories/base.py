from typing import Generic, Sequence, TypeVar
from sqlmodel import Session, SQLModel, select

T = TypeVar("T", bound=SQLModel)

class BaseRepository(Generic[T]):
    def __init__(self, model: type[T], session: Session):
        self.model = model
        self.session = session

    def get_by_id(self, id_val: int) -> T | None:
        return self.session.get(self.model, id_val)

    def get_all(self, offset: int = 0, limit: int | None = None) -> Sequence[T]:
        stmt = select(self.model).offset(offset)
        if limit is not None: stmt = stmt.limit(limit)
        return self.session.exec(stmt).all()

    def create(self, entity: T) -> T:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def save(self, entity: T) -> T:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def delete(self, entity: T) -> None:
        self.session.delete(entity)
        self.session.commit()
