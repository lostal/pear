from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.database import create_tables, engine
from app.dependencies import rate_limiter
from app.main import app
from app.models.usuario import Usuario


def _seed():
    create_tables()
    from app.core.security import hash_password
    with Session(engine) as s:
        if not s.exec(select(Usuario).where(Usuario.username == "admin")).first():
            s.add(Usuario(username="admin", password_hash=hash_password("admin123"), role="admin"))
            s.add(Usuario(username="user", password_hash=hash_password("user123"), role="user"))
            s.commit()


def _token(client, u="admin", p="admin123"):
    rate_limiter.attempts = {}
    r = client.post("/api/login", json={"username": u, "password": p})
    assert r.status_code == 200
    return r.json()["token"]


client = TestClient(app)


def test_login_admin():
    _seed()
    r = client.post("/api/login", json={"username": "admin", "password": "admin123"})
    assert r.status_code == 200
    assert "token" in r.json()


def test_login_bad():
    r = client.post("/api/login", json={"username": "admin", "password": "wrong"})
    assert r.status_code == 401
    assert r.json()["error"] == "Credenciales inválidas"


def test_productos_public():
    r = client.get("/api/productos")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_create_requires_admin():
    _seed()
    t = _token(client, "user", "user123")
    r = client.post("/api/productos", json={"nombre": "T", "precioBase": 10},
                    headers={"Authorization": f"Bearer {t}"})
    assert r.status_code == 403


def test_admin_create():
    _seed()
    t = _token(client)
    r = client.post("/api/productos", json={"nombre": "TP", "precioBase": 29.99},
                    headers={"Authorization": f"Bearer {t}"})
    assert r.status_code == 201
    assert r.json()["nombre"] == "TP"
    assert "_id" in r.json()


def test_users_requires_admin():
    _seed()
    t = _token(client, "user", "user123")
    assert client.get("/api/users", headers={"Authorization": f"Bearer {t}"}).status_code == 403


def test_admin_get_users():
    _seed()
    t = _token(client)
    r = client.get("/api/users", headers={"Authorization": f"Bearer {t}"})
    assert r.status_code == 200
    assert len(r.json()) >= 2
    assert "password" not in str(r.json())


def test_422():
    assert client.post("/api/login", json={"bad": "data"}).status_code == 422
