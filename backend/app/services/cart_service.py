from sqlmodel import Session
from app.models.cart_item import CartItem
from app.repositories.cart_repo import CartRepository

class CartService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = CartRepository(session)

    def get_cart(self, usuario_id: int) -> list[CartItem]:
        return self.repo.get_by_user(usuario_id)

    def add_to_cart(self, usuario_id: int, producto_id: int, color_valor: str | None = None, storage_valor: str | None = None) -> list[CartItem]:
        existing = self.repo.find_existing(usuario_id, producto_id, color_valor, storage_valor)
        if existing:
            existing.quantity += 1
            self.session.add(existing)
        else:
            self.session.add(CartItem(usuario_id=usuario_id, producto_id=producto_id, quantity=1,
                                      color_valor=color_valor if color_valor else None,
                                      storage_valor=storage_valor if storage_valor else None))
        self.session.commit()
        return self.repo.get_by_user(usuario_id)

    def remove_from_cart(self, usuario_id: int, producto_id: int) -> list[CartItem]:
        self.repo.remove_by_producto(usuario_id, producto_id)
        return self.repo.get_by_user(usuario_id)
