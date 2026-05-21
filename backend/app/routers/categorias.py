from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.core.database import get_session
from app.dependencies import require_admin
from app.schemas.categoria import CategoriaCreate, CategoriaReorder, CategoriaUpdate
from app.services.categoria_service import CategoriaService

router = APIRouter()

def _cat_to_dict(cat) -> dict:
    return {"_id": str(cat.id), "nombre": cat.nombre, "slug": cat.slug, "orden": cat.orden, "icono": cat.icono, "createdAt": cat.created_at.isoformat() if cat.created_at else None}

@router.get("")
def get_categorias(session: Session = Depends(get_session)):
    return [_cat_to_dict(c) for c in CategoriaService(session).get_all()]

@router.post("", status_code=status.HTTP_201_CREATED)
def create_categoria(data: CategoriaCreate, _admin=Depends(require_admin), session: Session = Depends(get_session)):
    try:
        return _cat_to_dict(CategoriaService(session).create(data.nombre, data.slug, data.orden, data.icono))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT if "Slug" in str(e) else status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/reorder")
def reorder_categorias(data: CategoriaReorder, _admin=Depends(require_admin), session: Session = Depends(get_session)):
    if not isinstance(data.ids, list): raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ids debe ser array")
    CategoriaService(session).reorder([str(i) for i in data.ids])
    return {"ok": True}

@router.put("/{cat_id}")
def update_categoria(cat_id: str, data: CategoriaUpdate, _admin=Depends(require_admin), session: Session = Depends(get_session)):
    try:
        return _cat_to_dict(CategoriaService(session).update(int(cat_id), **{k:v for k,v in data.model_dump().items() if v is not None}))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{cat_id}")
def delete_categoria(cat_id: str, _admin=Depends(require_admin), session: Session = Depends(get_session)):
    try:
        CategoriaService(session).delete(int(cat_id))
        return {"message": "Categoría eliminada"}
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
