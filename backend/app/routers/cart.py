from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.dependencies import get_current_user
from app.schemas.cart import CartAddRequest, CartItemPopulatedRead
from app.services.cart_service import CartService
from app.models.usuario import Usuario

router = APIRouter()

@router.get("")
def get_cart(current_user: Usuario = Depends(get_current_user), session: Session = Depends(get_session)):
    items = CartService(session).get_cart(current_user.id)
    return [CartItemPopulatedRead.from_cart_item(item).model_dump(by_alias=True) for item in items]

@router.post("/add")
def add_to_cart(data: CartAddRequest, current_user: Usuario = Depends(get_current_user), session: Session = Depends(get_session)):
    items = CartService(session).add_to_cart(current_user.id, int(data.productId), data.colorValor, data.storageValor)
    return [CartItemPopulatedRead.from_cart_item(item).model_dump(by_alias=True) for item in items]

@router.delete("/{product_id}")
def remove_from_cart(product_id: str, current_user: Usuario = Depends(get_current_user), session: Session = Depends(get_session)):
    items = CartService(session).remove_from_cart(current_user.id, int(product_id))
    return [CartItemPopulatedRead.from_cart_item(item).model_dump(by_alias=True) for item in items]
