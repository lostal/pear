# Servidor — Referencia

**IP:** `46.101.107.148`
**URL:** `https://pearstore.duckdns.org`
**Provider:** Digital Ocean (Droplet $12/mes, Ubuntu 24.04, 2GB RAM)

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

Esto hace: `git pull` + build del frontend + restart del backend.

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

# Reiniciar todo
docker compose -f /var/www/pear/docker-compose.prod.yml restart

# Parar todo
docker compose -f /var/www/pear/docker-compose.prod.yml down

# Levantar todo (desde cero o tras down)
cd /var/www/pear && docker compose -f docker-compose.prod.yml up -d --build
```

---

## Base de datos

### Exportar backup de MongoDB del servidor
```bash
docker exec mongo mongodump --db productos --out /tmp/dump
docker cp mongo:/tmp/dump ./dump_servidor
```

### Importar datos locales al servidor
En local:
```bash
docker exec mongo mongodump --db productos --out /tmp/dump
docker cp mongo:/tmp/dump ./dump
scp -r ./dump root@46.101.107.148:/tmp/dump
```
En el servidor:
```bash
docker cp /tmp/dump mongo:/tmp/dump
docker exec mongo mongorestore --db productos /tmp/dump/productos --drop
```

### Importar imágenes al servidor
En local:
```bash
scp -r ./backend/uploads root@46.101.107.148:/var/www/pear/backend/uploads
```
En el servidor:
```bash
docker cp /var/www/pear/backend/uploads/. backend:/app/uploads/
docker exec -u root backend chown -R node:node /app/uploads
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
