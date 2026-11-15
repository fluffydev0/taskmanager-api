from sqlalchemy.orm import Session

from app.features.auth.domain.entities import StoredUser
from app.features.auth.infrastructure.models import TokenRecord, UserRecord


def _to_stored(row: UserRecord) -> StoredUser:
    return StoredUser(id=row.id, username=row.username, password_hash=row.password_hash)


class SqlAlchemyUserRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_username(self, username: str) -> StoredUser | None:
        row = self._db.query(UserRecord).filter(UserRecord.username == username).first()
        return None if row is None else _to_stored(row)

    def get_by_id(self, user_id: int) -> StoredUser | None:
        row = self._db.query(UserRecord).filter(UserRecord.id == user_id).first()
        return None if row is None else _to_stored(row)

    def add(self, username: str, password_hash: str) -> StoredUser:
        row = UserRecord(username=username, password_hash=password_hash)
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return _to_stored(row)


class SqlAlchemyTokenRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def add(self, token: str, user_id: int) -> None:
        self._db.add(TokenRecord(token=token, user_id=user_id))
        self._db.commit()

    def get_user_id(self, token: str) -> int | None:
        row = self._db.query(TokenRecord).filter(TokenRecord.token == token).first()
        return None if row is None else row.user_id

    def delete(self, token: str) -> bool:
        row = self._db.query(TokenRecord).filter(TokenRecord.token == token).first()
        if row is None:
            return False
        self._db.delete(row)
        self._db.commit()
        return True
