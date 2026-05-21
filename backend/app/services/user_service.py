from sqlmodel import Session
from app.core.security import hash_password
from app.models.usuario import Usuario
from app.repositories.usuario_repo import UsuarioRepository

class UserService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = UsuarioRepository(session)

    def get_all(self) -> list[Usuario]:
        return list(self.repo.get_all())

    def create(self, username: str, password: str, role: str = "user") -> Usuario:
        existing = self.repo.get_by_username(username)
        if existing: raise ValueError("El nombre de usuario ya existe")
        return self.repo.create(Usuario(username=username, password_hash=hash_password(password), role=role))

    def update(self, id_val: int, **data) -> Usuario:
        user = self.repo.get_by_id(id_val)
        if not user: raise ValueError("Usuario no encontrado")
        if "username" in data and data["username"] is not None: user.username = data["username"]
        if "password" in data and data["password"] is not None: user.password_hash = hash_password(data["password"])
        if "role" in data and data["role"] is not None: user.role = data["role"]
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, id_val: int) -> None:
        user = self.repo.get_by_id(id_val)
        if not user: raise ValueError("Usuario no encontrado")
        self.repo.delete(user)
