from app.core.security import hash_password, new_token, password_matches
from app.features.auth.domain.entities import AuthToken, StoredUser, User
from app.features.auth.domain.exceptions import (
    InvalidCredentialsError,
    InvalidTokenError,
    UsernameTakenError,
)
from app.features.auth.domain.repositories import TokenRepository, UserRepository


def _to_user(row: StoredUser) -> User:
    return User(id=row.id, username=row.username)


class AuthService:
    def __init__(self, users: UserRepository, tokens: TokenRepository) -> None:
        self._users = users
        self._tokens = tokens

    def signup(self, username: str, password: str) -> User:
        if self._users.get_by_username(username) is not None:
            raise UsernameTakenError
        stored = self._users.add(username, hash_password(password))
        return _to_user(stored)

    def login(self, username: str, password: str) -> AuthToken:
        stored = self._users.get_by_username(username)
        if stored is None or not password_matches(password, stored.password_hash):
            raise InvalidCredentialsError
        token = new_token()
        self._tokens.add(token, stored.id)
        return AuthToken(access_token=token)

    def user_for_token(self, token: str) -> User:
        user_id = self._tokens.get_user_id(token)
        if user_id is None:
            raise InvalidTokenError
        stored = self._users.get_by_id(user_id)
        if stored is None:
            raise InvalidTokenError
        return _to_user(stored)

    def logout(self, token: str) -> None:
        if not self._tokens.delete(token):
            raise InvalidTokenError
