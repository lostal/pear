from sqlmodel import Session, select
from app.models.cart_item import CartItem
from app.repositories.base import BaseRepository

class CartRepository(BaseRepository[CartItem]):
    def __init__(self, session: Session):
        super().__init__(CartItem, session)

    def get_by_user(self, usuario_id: int) -> list[CartItem]:
        return list(self.session.exec(select(CartItem).where(CartItem.usuario_id == usuario_id)).all())

    def find_existing(self, usuario_id: int, producto_id: int, color: str | None, storage: str | None) -> CartItem | None:
        stmt = select(CartItem).where(CartItem.usuario_id == usuario_id, CartItem.producto_id == producto_id)
        items = list(self.session.exec(stmt).all())
        for item in items:
            if item.color_valor == color and item.storage_valor == storage:
                return item
        return None

    def remove_by_producto(self, usuario_id: int, producto_id: int) -> None:
        items = self.session.exec(select(CartItem).where(CartItem.usuario_id == usuario_id, CartItem.producto_id == producto_id)).all()
        for item in items:
            self.session.delete(item)
        self.session.commit()
