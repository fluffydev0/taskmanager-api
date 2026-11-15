from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from app.features.auth.application.service import AuthService
from app.features.auth.domain.entities import User
from app.features.auth.domain.exceptions import (
    InvalidCredentialsError,
    InvalidTokenError,
    UsernameTakenError,
)
from app.features.auth.presentation.dependencies import (
    _credentials_or_401,
    get_auth_service,
    get_current_user,
    security,
)
from app.features.auth.presentation.schemas import (
    AuthTokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.features.auth.presentation.views import render_token, render_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(body: UserCreate, auth: AuthService = Depends(get_auth_service)) -> UserResponse:
    try:
        user = auth.signup(body.username, body.password)
    except UsernameTakenError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken") from None
    return render_user(user)


@router.post("/login")
def login(body: UserLogin, auth: AuthService = Depends(get_auth_service)) -> AuthTokenResponse:
    try:
        token = auth.login(body.username, body.password)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        ) from None
    return render_token(token)


@router.get("/me")
def get_user(user: User = Depends(get_current_user)) -> UserResponse:
    return render_user(user)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    auth: AuthService = Depends(get_auth_service),
) -> None:
    token = _credentials_or_401(credentials).credentials
    try:
        auth.logout(token)
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated") from None
