from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlmodel import Session, select
from app.core.config import settings
from app.core.database import get_session
from app.models.producto import Producto

router = APIRouter()

@router.get("/sitemap.xml", response_class=Response)
def sitemap(session: Session = Depends(get_session)):
    productos = session.exec(select(Producto).where(Producto.activo == True)).all()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    urls = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url>\n    <loc>{settings.SITEMAP_DOMAIN}/</loc>\n    <changefreq>daily</changefreq>\n    <priority>1.0</priority>\n  </url>'
    for prod in productos:
        urls += f'\n  <url>\n    <loc>{settings.SITEMAP_DOMAIN}/producto/{prod.id}</loc>\n    <lastmod>{now}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>'
    urls += "\n</urlset>"
    return Response(content=urls, media_type="application/xml")
