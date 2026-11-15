from pydantic import BaseModel, Field

from app.features.tasks.domain.entities import TaskDraft


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None
    priority: int = Field(default=1, ge=1, le=5)
    complete: bool = False

    def to_draft(self) -> TaskDraft:
        return TaskDraft(
            title=self.title,
            description=self.description,
            priority=self.priority,
            complete=self.complete,
        )


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    priority: int
    complete: bool
