from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int
    username: str


@dataclass(frozen=True)
class StoredUser:
    id: int
    username: str
    password_hash: str


@dataclass(frozen=True)
class AuthToken:
    access_token: str
    token_type: str = "bearer"
