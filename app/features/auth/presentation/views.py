from app.features.auth.domain.entities import AuthToken, User
from app.features.auth.presentation.schemas import AuthTokenResponse, UserResponse


def render_user(user: User) -> UserResponse:
    return UserResponse(id=user.id, username=user.username)


def render_token(token: AuthToken) -> AuthTokenResponse:
    return AuthTokenResponse(access_token=token.access_token, token_type=token.token_type)
