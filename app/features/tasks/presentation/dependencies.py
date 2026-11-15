from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.features.tasks.application.service import TaskService
from app.features.tasks.domain.repositories import TaskRepository
from app.features.tasks.infrastructure.repository import SqlAlchemyTaskRepository


def get_task_repository(db: Session = Depends(get_db)) -> TaskRepository:
    return SqlAlchemyTaskRepository(db)


def get_task_service(tasks: TaskRepository = Depends(get_task_repository)) -> TaskService:
    return TaskService(tasks)
