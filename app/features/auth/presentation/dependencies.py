from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.auth.application.service import AuthService
from app.features.auth.domain.entities import User
from app.features.auth.domain.exceptions import InvalidTokenError
from app.features.auth.domain.repositories import TokenRepository, UserRepository
from app.features.auth.infrastructure.repository import (
    SqlAlchemyTokenRepository,
    SqlAlchemyUserRepository,
)

security = HTTPBearer(auto_error=False)


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return SqlAlchemyUserRepository(db)


def get_token_repository(db: Session = Depends(get_db)) -> TokenRepository:
    return SqlAlchemyTokenRepository(db)


def get_auth_service(
    users: UserRepository = Depends(get_user_repository),
    tokens: TokenRepository = Depends(get_token_repository),
) -> AuthService:
    return AuthService(users, tokens)


def _credentials_or_401(
    credentials: HTTPAuthorizationCredentials | None,
) -> HTTPAuthorizationCredentials:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return credentials


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    auth: AuthService = Depends(get_auth_service),
) -> User:
    token = _credentials_or_401(credentials).credentials
    try:
        return auth.user_for_token(token)
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated") from None
