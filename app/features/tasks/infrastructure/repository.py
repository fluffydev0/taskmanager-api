from sqlalchemy.orm import Session

from app.features.tasks.domain.entities import Task, TaskDraft
from app.features.tasks.infrastructure.models import TaskRecord


def _to_task(row: TaskRecord) -> Task:
    return Task(
        id=row.id,
        title=row.title,
        description=row.description,
        priority=row.priority,
        complete=row.complete,
    )


class SqlAlchemyTaskRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def all_for_owner(self, owner_id: int) -> list[Task]:
        rows = self._db.query(TaskRecord).filter(TaskRecord.owner_id == owner_id).all()
        return [_to_task(row) for row in rows]

    def get_for_owner(self, task_id: int, owner_id: int) -> Task | None:
        row = self._row(task_id, owner_id)
        return None if row is None else _to_task(row)

    def add(self, owner_id: int, data: TaskDraft) -> Task:
        row = TaskRecord(
            owner_id=owner_id,
            title=data.title,
            description=data.description,
            priority=data.priority,
            complete=data.complete,
        )
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return _to_task(row)

    def update(self, task_id: int, owner_id: int, data: TaskDraft) -> Task | None:
        row = self._row(task_id, owner_id)
        if row is None:
            return None
        row.title = data.title
        row.description = data.description
        row.priority = data.priority
        row.complete = data.complete
        self._db.commit()
        self._db.refresh(row)
        return _to_task(row)

    def delete(self, task_id: int, owner_id: int) -> bool:
        row = self._row(task_id, owner_id)
        if row is None:
            return False
        self._db.delete(row)
        self._db.commit()
        return True

    def _row(self, task_id: int, owner_id: int) -> TaskRecord | None:
        return (
            self._db.query(TaskRecord)
            .filter(TaskRecord.id == task_id, TaskRecord.owner_id == owner_id)
            .first()
        )
