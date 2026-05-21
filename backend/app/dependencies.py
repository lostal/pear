from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from app.core.database import engine, get_session
from app.core.security import verify_token
from app.repositories.usuario_repo import UsuarioRepository

security_scheme = HTTPBearer()

def get_db():
    with Session(engine) as session:
        yield session

def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security_scheme)],
    session: Annotated[Session, Depends(get_db)],
):
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_id = payload.get("id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    repo = UsuarioRepository(session)
    user = repo.get_by_id(int(user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user

def require_admin(
    current_user: Annotated["Usuario", Depends(get_current_user)],
):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo admin")
    return current_user

class RateLimiter:
    def __init__(self, max_attempts: int = 5, window_minutes: int = 15):
        self.max_attempts = max_attempts
        self.window_minutes = window_minutes
        self.attempts: dict[str, list] = {}

    def is_limited(self, key: str) -> bool:
        from datetime import datetime, timedelta, timezone
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(minutes=self.window_minutes)
        if key not in self.attempts:
            self.attempts[key] = []
        self.attempts[key] = [t for t in self.attempts[key] if t > cutoff]
        if len(self.attempts[key]) >= self.max_attempts:
            return True
        self.attempts[key].append(now)
        return False

rate_limiter = RateLimiter(max_attempts=5, window_minutes=15)
