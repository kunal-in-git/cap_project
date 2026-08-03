from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in-progress"
    done = "done"


class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.todo
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(BaseModel):
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.todo


class TaskStatusUpdate(BaseModel):
    status: TaskStatus
