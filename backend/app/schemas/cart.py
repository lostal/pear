from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class CartItemRead(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")
    productId: str
    quantity: int = 1
    colorValor: str | None = None
    storageValor: str | None = None

    @classmethod
    def from_cart_item(cls, item):
        return cls(_id=str(item.id), productId=str(item.producto_id),
                   quantity=item.quantity, colorValor=item.color_valor, storageValor=item.storage_valor)

class CartItemPopulatedRead(BaseModel):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    id: str = Field(alias="_id")
    productId: dict
    quantity: int = 1
    colorValor: str | None = None
    storageValor: str | None = None

    @classmethod
    def from_cart_item(cls, item):
        from app.schemas.producto import ProductoReadCart
        product_data = ProductoReadCart.from_producto(item.producto).model_dump(by_alias=True) if item.producto else None
        return cls(_id=str(item.id), productId=product_data, quantity=item.quantity,
                   colorValor=item.color_valor, storageValor=item.storage_valor)

class CartAddRequest(BaseModel):
    productId: str
    colorValor: str | None = None
    storageValor: str | None = None
