from app.features.tasks.domain.entities import Task, TaskDraft
from app.features.tasks.domain.exceptions import TaskNotFoundError
from app.features.tasks.domain.repositories import TaskRepository


class TaskService:
    def __init__(self, tasks: TaskRepository) -> None:
        self._tasks = tasks

    def all(self, owner_id: int) -> list[Task]:
        return self._tasks.all_for_owner(owner_id)

    def get(self, task_id: int, owner_id: int) -> Task:
        task = self._tasks.get_for_owner(task_id, owner_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    def create(self, data: TaskDraft, owner_id: int) -> Task:
        return self._tasks.add(owner_id, data)

    def update(self, task_id: int, data: TaskDraft, owner_id: int) -> Task:
        task = self._tasks.update(task_id, owner_id, data)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    def delete(self, task_id: int, owner_id: int) -> None:
        if not self._tasks.delete(task_id, owner_id):
            raise TaskNotFoundError(task_id)
