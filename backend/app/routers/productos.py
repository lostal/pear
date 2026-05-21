from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlmodel import Session
from app.core.database import get_session
from app.dependencies import require_admin
from app.schemas.producto import ImagenesReorder, ProductoCreate, ProductoRead, ProductoUpdate, ProductoReorder, GrupoCreate, GrupoUpdate, OpcionUpdate, OpcionReorder
from app.services.producto_service import ProductoService

router = APIRouter()

def _producto_to_dict(prod) -> dict:
    return ProductoRead.from_producto(prod).model_dump(by_alias=True)

@router.get("")
def get_productos(categoria: str | None = Query(default=None), session: Session = Depends(get_session)):
    return [_producto_to_dict(p) for p in ProductoService(session).get_all(categoria_slug=categoria)]

@router.post("", status_code=status.HTTP_201_CREATED)
def create_producto(data: ProductoCreate, _admin=Depends(require_admin), session: Session = Depends(get_session)):
    cat_id = int(data.categoria) if data.categoria else None
    return _producto_to_dict(ProductoService(session).create(data.nombre, data.descripcion, cat_id, data.precioBase, data.orden))

@router.put("/reorder")
def reorder_productos(data: ProductoReorder, _admin=Depends(require_admin), session: Session = Depends(get_session)):
    if not isinstance(data.ids, list): raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ids debe ser array")
    ProductoService(session).reorder([str(i) for i in data.ids])
    return {"ok": True}

@router.get("/{prod_id}")
def get_producto(prod_id: str, session: Session = Depends(get_session)):
    prod = ProductoService(session).get_by_id(int(prod_id))
    if not prod: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return _producto_to_dict(prod)

@router.put("/{prod_id}")
def update_producto(prod_id: str, data: ProductoUpdate, _admin=Depends(require_admin), session: Session = Depends(get_session)):
    try:
        return _producto_to_dict(ProductoService(session).update(int(prod_id), data.model_dump(exclude_none=True)))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{prod_id}")
def delete_producto(prod_id: str, _admin=Depends(require_admin), session: Session = Depends(get_session)):
    try:
        ProductoService(session).delete(int(prod_id))
        return {"message": "Producto eliminado"}
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

@router.post("/{prod_id}/imagenes-default")
async def add_imagenes_default(prod_id: str, _admin=Depends(require_admin), session: Session = Depends(get_session), imagenes: list[UploadFile] = File(default=[])):
    if not imagenes or (len(imagenes)==1 and imagenes[0].filename==""): raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sin archivos")
    return _producto_to_dict(ProductoService(session).add_imagenes_default(int(prod_id), imagenes))

@router.delete("/{prod_id}/imagenes-default")
def delete_imagen_default(prod_id: str, f: str = Query(..., alias="f"), _admin=Depends(require_admin), session: Session = Depends(get_session)):
    if not f: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Falta el parámetro f")
    return _producto_to_dict(ProductoService(session).delete_imagen_default(int(prod_id), f))

@router.put("/{prod_id}/imagenes-default")
def reorder_imagenes_default(prod_id: str, data: ImagenesReorder, _admin=Depends(require_admin), session: Session = Depends(get_session)):
    if not isinstance(data.imagenes, list): raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="imagenes debe ser array")
    return _producto_to_dict(ProductoService(session).reorder_imagenes_default(int(prod_id), data.imagenes))

@router.post("/{prod_id}/grupos", status_code=status.HTTP_201_CREATED)
def add_grupo(prod_id: str, data: GrupoCreate, _admin=Depends(require_admin), session: Session = Depends(get_session)):
    return _producto_to_dict(ProductoService(session).add_grupo(int(prod_id), data.tipo, data.nombre))

@router.put("/{prod_id}/grupos/{gid}")
def update_grupo(prod_id: str, gid: str, data: GrupoUpdate, _admin=Depends(require_admin), session: Session = Depends(get_session)):
    return _producto_to_dict(ProductoService(session).update_grupo(int(prod_id), int(gid), data.nombre, data.tipo))

@router.delete("/{prod_id}/grupos/{gid}")
def delete_grupo(prod_id: str, gid: str, _admin=Depends(require_admin), session: Session = Depends(get_session)):
    try:
        ProductoService(session).delete_grupo(int(prod_id), int(gid))
        return {"message": "Grupo eliminado"}
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grupo no encontrado")

@router.post("/{prod_id}/grupos/{gid}/opciones", status_code=status.HTTP_201_CREATED)
async def add_opcion(prod_id: str, gid: str, _admin=Depends(require_admin), session: Session = Depends(get_session), valor: str = Form(...), codigoHex: str | None = Form(default=None), modificadorPrecio: float = Form(default=0.0), imagenes: list[UploadFile] = File(default=[])):
    files = imagenes if imagenes and not (len(imagenes)==1 and imagenes[0].filename=="") else None
    return _producto_to_dict(ProductoService(session).add_opcion(int(prod_id), int(gid), valor, codigoHex, modificadorPrecio, files))

@router.put("/{prod_id}/grupos/{gid}/opciones/{oid}")
def update_opcion(prod_id: str, gid: str, oid: str, data: OpcionUpdate, _admin=Depends(require_admin), session: Session = Depends(get_session)):
    try:
        return _producto_to_dict(ProductoService(session).update_opcion(int(prod_id), int(gid), int(oid), **data.model_dump(exclude_none=True)))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{prod_id}/grupos/{gid}/opciones/{oid}")
def delete_opcion(prod_id: str, gid: str, oid: str, _admin=Depends(require_admin), session: Session = Depends(get_session)):
    try:
        ProductoService(session).delete_opcion(int(prod_id), int(gid), int(oid))
        return {"message": "Opción eliminada"}
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Opción no encontrada")

@router.put("/{prod_id}/grupos/{gid}/opciones")
def reorder_opciones(prod_id: str, gid: str, data: OpcionReorder, _admin=Depends(require_admin), session: Session = Depends(get_session)):
    if not isinstance(data.opcionIds, list): raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="opcionIds debe ser array")
    try:
        return _producto_to_dict(ProductoService(session).reorder_opciones(int(prod_id), int(gid), [str(oid) for oid in data.opcionIds]))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/{prod_id}/grupos/{gid}/opciones/{oid}/imagenes")
async def add_imagenes_opcion(prod_id: str, gid: str, oid: str, _admin=Depends(require_admin), session: Session = Depends(get_session), imagenes: list[UploadFile] = File(default=[])):
    if not imagenes or (len(imagenes)==1 and imagenes[0].filename==""): raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sin archivos")
    return _producto_to_dict(ProductoService(session).add_imagenes_opcion(int(prod_id), int(gid), int(oid), imagenes))

@router.delete("/{prod_id}/grupos/{gid}/opciones/{oid}/imagenes")
def delete_imagen_opcion(prod_id: str, gid: str, oid: str, f: str = Query(..., alias="f"), _admin=Depends(require_admin), session: Session = Depends(get_session)):
    if not f: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Falta el parámetro f")
    return _producto_to_dict(ProductoService(session).delete_imagen_opcion(int(prod_id), int(gid), int(oid), f))

@router.put("/{prod_id}/grupos/{gid}/opciones/{oid}/imagenes")
def reorder_imagenes_opcion(prod_id: str, gid: str, oid: str, data: ImagenesReorder, _admin=Depends(require_admin), session: Session = Depends(get_session)):
    if not isinstance(data.imagenes, list): raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="imagenes debe ser array")
    return _producto_to_dict(ProductoService(session).reorder_imagenes_opcion(int(prod_id), int(gid), int(oid), data.imagenes))
