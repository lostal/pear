from pydantic import BaseModel, ConfigDict, Field

class CartItemSimple(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")
    productId: str
    quantity: int = 1
    colorValor: str | None = None
    storageValor: str | None = None

class UsuarioRead(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")
    username: str
    role: str = "user"
    cart: list[CartItemSimple] = []

    @classmethod
    def from_usuario(cls, user):
        return cls(_id=str(user.id), username=user.username, role=user.role,
                   cart=[CartItemSimple(_id=str(item.id), productId=str(item.producto_id),
                         quantity=item.quantity, colorValor=item.color_valor, storageValor=item.storage_valor)
                         for item in (user.cart_items or [])])

class UsuarioCreate(BaseModel):
    username: str
    password: str
    role: str = "user"

class UsuarioUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    role: str | None = None
