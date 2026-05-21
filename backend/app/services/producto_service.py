import os, shutil, time
from pathlib import Path
from sqlmodel import Session
from app.core.config import settings
from app.models.producto import Producto
from app.models.producto_imagen import ProductoImagenDefault
from app.models.grupo_opcion import GrupoOpcion
from app.models.opcion import Opcion
from app.models.opcion_imagen import OpcionImagen
from app.repositories.producto_repo import ProductoRepository

UPLOADS_ROOT = Path(settings.UPLOADS_DIR)

def _save_upload_file(file, product_id: int, subdir: str) -> str:
    ext = Path(file.filename).suffix if file.filename else ""
    filename = f"{int(time.time() * 1000)}{ext}"
    dest_dir = UPLOADS_ROOT / "productos" / str(product_id) / subdir
    dest_dir.mkdir(parents=True, exist_ok=True)
    with open(dest_dir / filename, "wb") as f:
        f.write(file.file.read())
    return str(Path("productos") / str(product_id) / subdir / filename).replace("\\", "/")

def _delete_file(rel_path: str) -> None:
    try:
        fp = UPLOADS_ROOT / rel_path
        if fp.exists(): os.remove(fp)
    except OSError: pass

def _delete_product_dir(product_id: int) -> None:
    try:
        d = UPLOADS_ROOT / "productos" / str(product_id)
        if d.exists(): shutil.rmtree(d)
    except OSError: pass

class ProductoService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = ProductoRepository(session)

    def get_all(self, categoria_slug: str | None = None) -> list[Producto]:
        return self.repo.get_all_active(categoria_slug)

    def get_by_id(self, id_val: int) -> Producto | None:
        return self.repo.get_by_id_with_relations(id_val)

    def create(self, nombre: str, descripcion: str, categoria_id: int | None, precio_base: float, orden: int = 0) -> Producto:
        return self.repo.create(Producto(nombre=nombre, descripcion=descripcion, categoria_id=categoria_id, precio_base=precio_base, orden=orden))

    def update(self, id_val: int, data: dict) -> Producto:
        mapped = {}
        if "nombre" in data and data["nombre"] is not None: mapped["nombre"] = data["nombre"]
        if "descripcion" in data and data["descripcion"] is not None: mapped["descripcion"] = data["descripcion"]
        if "categoria" in data and data["categoria"] is not None: mapped["categoria_id"] = int(data["categoria"]) if data["categoria"] else None
        if "precioBase" in data and data["precioBase"] is not None: mapped["precio_base"] = data["precioBase"]
        if "activo" in data and data["activo"] is not None: mapped["activo"] = data["activo"]
        if "orden" in data and data["orden"] is not None: mapped["orden"] = data["orden"]
        prod = self.repo.update_by_id(id_val, mapped)
        if not prod: raise ValueError("Producto no encontrado")
        return prod

    def delete(self, id_val: int) -> None:
        if not self.repo.get_by_id_with_relations(id_val): raise ValueError("Producto no encontrado")
        _delete_product_dir(id_val)
        self.repo.delete_by_id(id_val)

    def reorder(self, ids: list[str]) -> None:
        self.repo.reorder(ids)

    def add_imagenes_default(self, product_id: int, files: list) -> Producto:
        prod = self.repo.get_by_id_with_relations(product_id)
        if not prod: raise ValueError("Producto no encontrado")
        if not files: raise ValueError("Sin archivos")
        for f in files:
            self.session.add(ProductoImagenDefault(producto_id=product_id, imagen=_save_upload_file(f, product_id, "default"), orden=len(prod.imagenes_default)))
        self.session.commit()
        self.session.refresh(prod)
        return prod

    def delete_imagen_default(self, product_id: int, filename: str) -> Producto:
        prod = self.repo.get_by_id_with_relations(product_id)
        for img in (prod.imagenes_default or []):
            if img.imagen == filename:
                _delete_file(img.imagen)
                self.session.delete(img)
                self.session.commit()
                self.session.refresh(prod)
                return prod
        return prod

    def reorder_imagenes_default(self, product_id: int, imagenes: list[str]) -> Producto:
        prod = self.repo.get_by_id_with_relations(product_id)
        existing = {img.imagen: img for img in (prod.imagenes_default or [])}
        for i, ip in enumerate(imagenes):
            if ip in existing: existing[ip].orden = i; self.session.add(existing[ip])
        self.session.commit()
        self.session.refresh(prod)
        return prod

    def add_grupo(self, product_id: int, tipo: str, nombre: str) -> Producto:
        prod = self.repo.get_by_id_with_relations(product_id)
        self.session.add(GrupoOpcion(producto_id=product_id, tipo=tipo, nombre=nombre, orden=len(prod.grupos_opciones or [])))
        self.session.commit()
        self.session.refresh(prod)
        return prod

    def update_grupo(self, product_id: int, grupo_id: int, nombre: str = None, tipo: str = None) -> Producto:
        prod = self.repo.get_by_id_with_relations(product_id)
        for g in (prod.grupos_opciones or []):
            if g.id == grupo_id:
                if nombre is not None: g.nombre = nombre
                if tipo is not None: g.tipo = tipo
                self.session.add(g)
                self.session.commit()
                self.session.refresh(prod)
                return prod
        raise ValueError("Grupo no encontrado")

    def delete_grupo(self, product_id: int, grupo_id: int) -> None:
        prod = self.repo.get_by_id_with_relations(product_id)
        for g in (prod.grupos_opciones or []):
            if g.id == grupo_id:
                if g.tipo == "color":
                    for op in (g.opciones or []):
                        for img in (op.imagenes or []):
                            _delete_file(img.imagen)
                self.session.delete(g)
                self.session.commit()
                return
        raise ValueError("Grupo no encontrado")

    def add_opcion(self, product_id: int, grupo_id: int, valor: str, codigo_hex: str = None, modificador_precio: float = 0.0, files: list = None) -> Producto:
        prod = self.repo.get_by_id_with_relations(product_id)
        grupo = next((g for g in (prod.grupos_opciones or []) if g.id == grupo_id), None)
        if not grupo: raise ValueError("Grupo no encontrado")
        op = Opcion(grupo_id=grupo_id, valor=valor, codigo_hex=codigo_hex, modificador_precio=modificador_precio, orden=len(grupo.opciones or []))
        self.session.add(op)
        self.session.flush()
        if files:
            for f in files:
                self.session.add(OpcionImagen(opcion_id=op.id, imagen=_save_upload_file(f, product_id, str(op.id)), orden=0))
        self.session.commit()
        self.session.refresh(prod)
        return prod

    def update_opcion(self, product_id: int, grupo_id: int, opcion_id: int, **data) -> Producto:
        op = self.session.get(Opcion, opcion_id)
        if not op: raise ValueError("Opción no encontrada")
        if "valor" in data and data["valor"] is not None: op.valor = data["valor"]
        if "codigoHex" in data: op.codigo_hex = data["codigoHex"]
        if "modificadorPrecio" in data and data["modificadorPrecio"] is not None: op.modificador_precio = data["modificadorPrecio"]
        self.session.add(op)
        self.session.commit()
        return self.repo.get_by_id_with_relations(product_id)

    def delete_opcion(self, product_id: int, grupo_id: int, opcion_id: int) -> None:
        op = self.session.get(Opcion, opcion_id)
        if not op: raise ValueError("Opción no encontrada")
        for img in (op.imagenes or []): _delete_file(img.imagen)
        self.session.delete(op)
        self.session.commit()

    def reorder_opciones(self, product_id: int, grupo_id: int, opcion_ids: list[str]) -> Producto:
        prod = self.repo.get_by_id_with_relations(product_id)
        grupo = next((g for g in (prod.grupos_opciones or []) if g.id == grupo_id), None)
        if not grupo: raise ValueError("Grupo no encontrado")
        omap = {str(op.id): op for op in (grupo.opciones or [])}
        for i, oid in enumerate(opcion_ids):
            if oid in omap: omap[oid].orden = i; self.session.add(omap[oid])
        self.session.commit()
        self.session.refresh(prod)
        return prod

    def add_imagenes_opcion(self, product_id: int, grupo_id: int, opcion_id: int, files: list) -> Producto:
        op = self.session.get(Opcion, opcion_id)
        if not op: raise ValueError("Opción no encontrada")
        if not files: raise ValueError("Sin archivos")
        for f in files:
            self.session.add(OpcionImagen(opcion_id=opcion_id, imagen=_save_upload_file(f, product_id, str(opcion_id)), orden=0))
        self.session.commit()
        return self.repo.get_by_id_with_relations(product_id)

    def delete_imagen_opcion(self, product_id: int, grupo_id: int, opcion_id: int, filename: str) -> Producto:
        op = self.session.get(Opcion, opcion_id)
        for img in (op.imagenes or []):
            if img.imagen == filename:
                _delete_file(img.imagen)
                self.session.delete(img)
                self.session.commit()
                break
        return self.repo.get_by_id_with_relations(product_id)

    def reorder_imagenes_opcion(self, product_id: int, grupo_id: int, opcion_id: int, imagenes: list[str]) -> Producto:
        op = self.session.get(Opcion, opcion_id)
        existing = {img.imagen: img for img in (op.imagenes or [])}
        for i, ip in enumerate(imagenes):
            if ip in existing: existing[ip].orden = i; self.session.add(existing[ip])
        self.session.commit()
        return self.repo.get_by_id_with_relations(product_id)
