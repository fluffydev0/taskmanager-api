from fastapi import APIRouter, Depends, HTTPException, status

from app.features.auth.domain.entities import User
from app.features.auth.presentation.dependencies import get_current_user
from app.features.tasks.application.service import TaskService
from app.features.tasks.domain.exceptions import TaskNotFoundError
from app.features.tasks.presentation.dependencies import get_task_service
from app.features.tasks.presentation.schemas import TaskCreate, TaskResponse
from app.features.tasks.presentation.views import render_task, render_tasks

router = APIRouter(prefix="/tasks", tags=["tasks"])


def _not_found() -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@router.get("")
def list_tasks(
    task_service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user),
) -> list[TaskResponse]:
    return render_tasks(task_service.all(user.id))


@router.get("/{task_id}")
def get_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user),
) -> TaskResponse:
    try:
        task = task_service.get(task_id, user.id)
    except TaskNotFoundError:
        raise _not_found() from None
    return render_task(task)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(
    body: TaskCreate,
    task_service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user),
) -> TaskResponse:
    return render_task(task_service.create(body.to_draft(), user.id))


@router.put("/{task_id}")
def update_task(
    task_id: int,
    body: TaskCreate,
    task_service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user),
) -> TaskResponse:
    try:
        task = task_service.update(task_id, body.to_draft(), user.id)
    except TaskNotFoundError:
        raise _not_found() from None
    return render_task(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service),
    user: User = Depends(get_current_user),
) -> None:
    try:
        task_service.delete(task_id, user.id)
    except TaskNotFoundError:
        raise _not_found() from None
