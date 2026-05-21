from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session
from app.core.database import get_session
from app.dependencies import rate_limiter
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, MessageResponse
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, session: Session = Depends(get_session)):
    try:
        AuthService(session).register(data.username, data.password)
        return {"message": "Usuario registrado con éxito"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, request: Request, session: Session = Depends(get_session)):
    client_ip = request.client.host if request.client else "unknown"
    if rate_limiter.is_limited(client_ip):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Has superado el límite de intentos. Vuelve a intentarlo en 15 minutos.")
    token = AuthService(session).login(data.username, data.password)
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    return {"token": token}
