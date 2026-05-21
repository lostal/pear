from typing import Optional
from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

class CartItem(SQLModel, table=True):
    __tablename__ = "cart_item"
    __table_args__ = (UniqueConstraint("usuario_id", "producto_id", "color_valor", "storage_valor", name="uq_cart_item"),)
    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", ondelete="CASCADE", index=True)
    producto_id: int = Field(foreign_key="producto.id", ondelete="CASCADE", index=True)
    quantity: int = Field(default=1)
    color_valor: str | None = Field(default=None, max_length=100)
    storage_valor: str | None = Field(default=None, max_length=100)
    usuario: Optional["Usuario"] = Relationship(back_populates="cart_items")
    producto: Optional["Producto"] = Relationship(sa_relationship_kwargs={"lazy": "selectin"})
