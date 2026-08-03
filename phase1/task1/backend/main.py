from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import Task, TaskCreate, TaskStatusUpdate

app = FastAPI(title="Task Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks: dict[UUID, Task] = {}


def get_task_or_404(task_id: UUID) -> Task:
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task_in: TaskCreate) -> Task:
    task = Task(**task_in.model_dump())
    tasks[task.id] = task
    return task


@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    return list(tasks.values())


@app.put("/tasks/{task_id}", response_model=Task)
def update_task_status(task_id: UUID, update: TaskStatusUpdate) -> Task:
    task = get_task_or_404(task_id)
    task.status = update.status
    return task


@app.delete("/tasks/{task_id}", response_model=Task, status_code=200)
def delete_task(task_id: UUID) -> None:
    task = get_task_or_404(task_id)
    del tasks[task_id]
    return task
