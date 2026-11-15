from dataclasses import dataclass


@dataclass(frozen=True)
class TaskDraft:
    title: str
    description: str | None
    priority: int
    complete: bool


@dataclass(frozen=True)
class Task:
    id: int
    title: str
    description: str | None
    priority: int
    complete: bool
