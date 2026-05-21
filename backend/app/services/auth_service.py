from sqlmodel import Session
from app.core.security import hash_password, verify_password, create_access_token
from app.models.usuario import Usuario
from app.repositories.usuario_repo import UsuarioRepository

class AuthService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = UsuarioRepository(session)

    def register(self, username: str, password: str) -> Usuario:
        existing = self.repo.get_by_username(username)
        if existing: raise ValueError("El nombre de usuario ya existe")
        user = Usuario(username=username, password_hash=hash_password(password), role="user")
        return self.repo.create(user)

    def login(self, username: str, password: str) -> str | None:
        user = self.repo.get_by_username(username)
        if not user: return None
        if not verify_password(password, user.password_hash): return None
        return create_access_token(data={"id": str(user.id), "username": user.username, "role": user.role})
