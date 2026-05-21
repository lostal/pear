import shutil
from datetime import datetime, timezone
from pathlib import Path
from pymongo import MongoClient
from sqlmodel import Session, select
from app.core.database import create_tables, engine
from app.models.categoria import Categoria
from app.models.cart_item import CartItem
from app.models.grupo_opcion import GrupoOpcion
from app.models.opcion import Opcion
from app.models.opcion_imagen import OpcionImagen
from app.models.producto import Producto
from app.models.producto_imagen import ProductoImagenDefault
from app.models.usuario import Usuario

MONGO_URI = "mongodb://localhost:27017/productos"
OLD_UPLOADS = Path("../backend/uploads")
NEW_UPLOADS = Path("uploads")
id_map = {}

def _transform_path(old_path, old_id, new_id, old_oid=None, new_oid=None):
    parts = old_path.replace("\\","/").split("/")
    if old_oid and new_oid:
        parts = [str(new_id) if p==old_id else (str(new_oid) if p==old_oid else p) for p in parts]
    else:
        parts = [str(new_id) if p==old_id else p for p in parts]
    return "/".join(parts)

def migrate():
    create_tables()
    client = MongoClient(MONGO_URI)
    db = client["productos"]
    with Session(engine) as session:
        if session.exec(select(Usuario)).first():
            print("DB already has data. Delete pear.db first."); return
        now = datetime.now(timezone.utc)
        for cat_data in db.categorias.find().sort("orden", 1):
            cat = Categoria(nombre=cat_data["nombre"], slug=cat_data["slug"], orden=cat_data.get("orden",0), icono=cat_data.get("icono"), created_at=cat_data.get("createdAt",now))
            session.add(cat); session.flush()
            id_map[str(cat_data["_id"])] = cat.id
        session.commit()
        print(f"Migrated {len(id_map)} categories")
        count = 0
        for prod_data in db.productos.find().sort("orden", 1):
            new_cat_id = id_map.get(str(prod_data["categoria"])) if prod_data.get("categoria") else None
            prod = Producto(nombre=prod_data["nombre"], descripcion=prod_data.get("descripcion",""), categoria_id=new_cat_id, precio_base=prod_data.get("precioBase",0), activo=prod_data.get("activo",True), orden=prod_data.get("orden",0), created_at=prod_data.get("createdAt",now), updated_at=prod_data.get("updatedAt"))
            session.add(prod); session.flush()
            new_id, old_id = prod.id, str(prod_data["_id"])
            id_map[old_id] = new_id; count += 1
            old_dir = OLD_UPLOADS / "productos" / old_id
            new_dir = NEW_UPLOADS / "productos" / str(new_id)
            if old_dir.exists(): shutil.copytree(old_dir, new_dir, dirs_exist_ok=True)
            for g_idx, gd in enumerate(prod_data.get("gruposOpciones",[]) or []):
                grupo = GrupoOpcion(producto_id=new_id, tipo=gd["tipo"], nombre=gd["nombre"], orden=g_idx)
                session.add(grupo); session.flush()
                old_gid = str(gd["_id"])
                for o_idx, od in enumerate(gd.get("opciones",[]) or []):
                    op = Opcion(grupo_id=grupo.id, valor=od["valor"], codigo_hex=od.get("codigoHex"), modificador_precio=od.get("modificadorPrecio",0), orden=o_idx)
                    session.add(op); session.flush()
                    old_oid = str(od["_id"])
                    old_opt_dir = old_dir / old_oid
                    new_opt_dir = new_dir / str(op.id)
                    if old_opt_dir.exists(): shutil.copytree(old_opt_dir, new_opt_dir, dirs_exist_ok=True)
                    for ii, old_img in enumerate(od.get("imagenes",[]) or []):
                        session.add(OpcionImagen(opcion_id=op.id, imagen=_transform_path(old_img, old_id, new_id, old_oid, op.id), orden=ii))
            for i, old_img in enumerate(prod_data.get("imagenesDefault",[]) or []):
                session.add(ProductoImagenDefault(producto_id=new_id, imagen=_transform_path(old_img, old_id, new_id), orden=i))
        session.commit()
        print(f"Migrated {count} products")
        uc = 0
        for user_data in db.users.find():
            u = Usuario(username=user_data["username"], password_hash=user_data["password"], role=user_data.get("role","user"))
            session.add(u); session.flush()
            id_map[str(user_data["_id"])] = u.id; uc += 1
            for ci in user_data.get("cart",[]) or []:
                pid = id_map.get(str(ci["productId"]))
                if pid: session.add(CartItem(usuario_id=u.id, producto_id=pid, quantity=ci.get("quantity",1), color_valor=ci.get("colorValor"), storage_valor=ci.get("storageValor")))
        session.commit()
        print(f"Migrated {uc} users with carts")
    client.close()
    print("Migration complete!")

if __name__ == "__main__":
    migrate()
