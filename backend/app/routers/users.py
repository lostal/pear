from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.core.database import get_session
from app.dependencies import require_admin
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.services.user_service import UserService

router = APIRouter()

def _user_to_dict(user) -> dict:
    return {"_id": str(user.id), "username": user.username, "role": user.role,
            "cart": [{"_id": str(item.id), "productId": str(item.producto_id), "quantity": item.quantity,
                       "colorValor": item.color_valor, "storageValor": item.storage_valor}
                     for item in (user.cart_items or [])]}

@router.get("")
def get_users(_admin=Depends(require_admin), session: Session = Depends(get_session)):
    return [_user_to_dict(u) for u in UserService(session).get_all()]

@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(data: UsuarioCreate, _admin=Depends(require_admin), session: Session = Depends(get_session)):
    try:
        user = UserService(session).create(data.username, data.password, data.role)
        return {"message": "Usuario creado con éxito", "user": {"username": user.username, "role": user.role}}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{user_id}")
def update_user(user_id: str, data: UsuarioUpdate, _admin=Depends(require_admin), session: Session = Depends(get_session)):
    try:
        return _user_to_dict(UserService(session).update(int(user_id), **{k:v for k,v in data.model_dump().items() if v is not None}))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{user_id}")
def delete_user(user_id: str, _admin=Depends(require_admin), session: Session = Depends(get_session)):
    try:
        UserService(session).delete(int(user_id))
        return {"message": "Usuario eliminado"}
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
