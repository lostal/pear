# Servidor — Referencia

**IP:** `46.101.107.148`
**URL:** `https://pearstore.duckdns.org`
**Provider:** Digital Ocean (Droplet $12/mes, Ubuntu 24.04, 2GB RAM)

---

## Stack actual

| Capa     | Tecnología                    |
| -------- | ----------------------------- |
| Backend  | Python 3.13, FastAPI, SQLite  |
| Frontend | Svelte 5 (SPA estática)       |
| Proxy    | Nginx + Certbot               |
| DB       | SQLite (archivo en volumen)   |

---

## Conectarse al servidor

```bash
ssh root@46.101.107.148
```

---

## Desplegar cambios

Después de hacer `git push` desde local, en el servidor:

```bash
/var/www/pear/deploy.sh
```

Esto hace: `git pull` + build del frontend + rebuild y restart del backend Docker.

---

## Ver logs

```bash
# Backend (últimas 50 líneas)
docker logs backend --tail 50

# En tiempo real
docker logs backend -f

# Nginx
tail -f /var/log/nginx/error.log
```

---

## Gestionar contenedores

```bash
# Ver estado
docker compose -f /var/www/pear/docker-compose.prod.yml ps

# Reiniciar backend
docker compose -f /var/www/pear/docker-compose.prod.yml restart backend

# Parar todo
docker compose -f /var/www/pear/docker-compose.prod.yml down

# Levantar todo
cd /var/www/pear && docker compose -f docker-compose.prod.yml up -d --build
```

---

## Base de datos (SQLite)

El archivo `pear.db` se persiste en el volumen `data/db/` del host.

### Backup manual
```bash
cp /var/www/pear/data/db/pear.db /var/www/pear/data/db/pear_$(date +%Y%m%d).db
```

### Restaurar backup
```bash
cp /var/www/pear/data/db/pear_20260521.db /var/www/pear/data/db/pear.db
docker compose -f /var/www/pear/docker-compose.prod.yml restart backend
```

---

## Subir archivos locales al servidor

```bash
# Imágenes de productos
scp -r ./backend/uploads/productos root@46.101.107.148:/var/www/pear/data/uploads/

# Base de datos
scp ./backend/pear.db root@46.101.107.148:/var/www/pear/data/db/
```

---

## Certificado SSL

Se renueva automáticamente. Para forzar renovación manual:
```bash
certbot renew
```

Expira el **2026-06-21** (renovación automática activa).

---

## Añadir otra app al servidor

1. Clonar repo en `/var/www/nombre-app`
2. Levantar con Docker Compose
3. Crear config nginx en `/etc/nginx/sites-available/nombre-app`
4. Activar: `ln -s /etc/nginx/sites-available/nombre-app /etc/nginx/sites-enabled/`
5. Certificado: `certbot --nginx -d subdominio.duckdns.org`
