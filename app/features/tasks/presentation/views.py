from app.features.tasks.domain.entities import Task
from app.features.tasks.presentation.schemas import TaskResponse


def render_task(task: Task) -> TaskResponse:
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        priority=task.priority,
        complete=task.complete,
    )


def render_tasks(tasks: list[Task]) -> list[TaskResponse]:
    return [render_task(task) for task in tasks]
