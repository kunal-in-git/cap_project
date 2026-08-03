# Task D — AI-Gated SDLC Flow Document

**Feature chosen:** Update Task Status — moving a task through `todo` → `in-progress` → `done` via the "Advance Status" button in the UI, backed by `PUT /tasks/{id}` in the [Task Manager app](../task1/README.md).

This document walks the full SDLC for that one feature, with the actual prompt used at each stage and the actual output. Supporting artifacts (a standalone test file, a Dockerfile, a CI config) live in [`artifacts/`](artifacts/) and were each run for real against the live `task1` code — not just described.

---

## 1. Requirements

**Prompt (to Claude):**
> Write a short PRD for an "Update Task Status" feature in a Task Manager app. The feature lets a user move a task through todo → in-progress → done via a button in the UI, backed by a `PUT /tasks/{id}` endpoint. Include: problem statement, goal, user story, acceptance criteria, non-goals.

**Output:**
> **Problem:** Tasks currently have a status field but no way to change it after creation — the app can only create, list, and delete tasks.
>
> **Goal:** Let a user advance a task's status without leaving the task list, using a single click.
>
> **User story:** As a user managing my task list, I want to mark a task as in-progress or done so the list reflects real progress.
>
> **Acceptance criteria:**
> - A `PUT /tasks/{id}` endpoint accepts a new status and returns the updated task.
> - An unknown `id` returns 404.
> - An invalid status value is rejected before it reaches the in-memory store.
> - The UI exposes a button that advances the task to the next status in the cycle (`todo` → `in-progress` → `done` → `todo`).
> - Other task fields (`title`, `description`, `created_at`) are unchanged by the update.
>
> **Non-goals:** Bulk status updates, status change history/audit log, and role-based permissions on who can change a status are out of scope for this feature.

---

## 2. Design

**Prompt:**
> Given the existing `Task` model (`id`, `title`, `description`, `status` enum, `created_at`) and the React `TaskItem` component, sketch the data model and component structure needed to support updating a task's status.

**Output:**
> Data model — a narrow request model instead of reusing `TaskCreate`, so the endpoint can't accidentally overwrite `title`/`description`:
> ```
> TaskStatusUpdate { status: TaskStatus }
> ```
>
> Component/request flow:
> ```
> TaskItem (button: "Advance Status")
>   → onUpdateStatus(id, nextStatus(status))      [App.jsx handler]
>     → updateTaskStatus(id, status)              [api.js]
>       → PUT /tasks/{id}  { status }              [main.py]
>         → tasks[id].status = status
>         → 404 if id not found
>       ← updated Task JSON
>     ← App re-fetches the task list (getTasks)
>   ← TaskList re-renders with the new status badge
> ```
> `nextStatus()` is pure client-side cycling logic (`todo → in-progress → done → todo`); the server only ever validates and applies whatever status it's sent, it doesn't own the "next" logic. That keeps the endpoint reusable if a future UI wants to jump straight to a specific status instead of cycling.

---

## 3. Coding

**Which parts were AI-generated:** all of it — the Pydantic model, the endpoint, and the React button/handler were written by Claude as part of building `task1`.

**Prompt:**
> Generate the FastAPI PUT endpoint and Pydantic model needed to update a task's status by id, returning 404 if not found.

**Output** (from [`task1/backend/models.py`](../task1/backend/models.py) and [`task1/backend/main.py`](../task1/backend/main.py)):
```python
class TaskStatusUpdate(BaseModel):
    status: TaskStatus


@app.put("/tasks/{task_id}", response_model=Task)
def update_task_status(task_id: UUID, update: TaskStatusUpdate) -> Task:
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = update.status
    return task
```

**Prompt:**
> Generate a React `TaskItem` component with a button that advances a task's status through todo → in-progress → done and calls an update callback.

**Output** (from [`task1/frontend/src/components/TaskItem.jsx`](../task1/frontend/src/components/TaskItem.jsx)):
```jsx
const STATUS_ORDER = ["todo", "in-progress", "done"];

function nextStatus(status) {
  const idx = STATUS_ORDER.indexOf(status);
  return STATUS_ORDER[(idx + 1) % STATUS_ORDER.length];
}

// ...
<button onClick={() => onUpdateStatus(task.id, nextStatus(task.status))}>
  Advance Status
</button>
```

---

## 4. Testing

**Prompt:**
> Suggest test cases for the PUT /tasks/{id} update-status endpoint.

**AI-suggested cases:**
1. Update an existing task's status to `in-progress` → 200, status changed.
2. Update to `done` → 200, status changed.
3. Updated status is reflected in a subsequent `GET /tasks`.
4. Unknown task id → 404.
5. Invalid status value (not in the enum) → 422.

**Did it miss any edge cases?** Yes — three, found while actually writing the tests rather than just listing them:
- **Malformed id, not just unknown id.** A path param that isn't a valid UUID at all (e.g. `not-a-uuid`) fails FastAPI's parameter parsing before the route body runs, so it's a **422**, not the 404 the first pass assumed.
- **Idempotency.** Sending the same status twice in a row should succeed both times with no side effect — not obviously true until it's checked, since the handler has no early-return for "already in that state."
- **No forward-only guard.** The endpoint has no state machine — `done` → `todo` is currently accepted. Not necessarily a bug, but worth calling out since the PRD's "advance" framing implies forward motion only, and the implementation doesn't enforce that.

All 8 cases (the 5 suggested + 3 missed) are implemented in [`artifacts/test_update_task_status.py`](artifacts/test_update_task_status.py) and were actually run against the live `task1/backend` code:

```
$ pytest test_update_task_status.py -v
test_update_status_to_in_progress PASSED
test_update_status_to_done PASSED
test_update_status_persists_in_list PASSED
test_update_status_unknown_task_returns_404 PASSED
test_update_status_invalid_enum_value_returns_422 PASSED
test_update_status_malformed_id_returns_422_not_404 PASSED
test_update_status_is_idempotent PASSED
test_update_status_can_move_backward PASSED
======================== 8 passed in 0.19s ========================
```

---

## 5. Deployment

**Prompt:**
> Generate a Dockerfile for this FastAPI backend suitable for a simple deployment, and a GitHub Actions workflow that runs tests and builds the image on every push.

**Output — [`artifacts/Dockerfile`](artifacts/Dockerfile):**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Output — [`artifacts/ci.yml`](artifacts/ci.yml):** a two-job workflow (`test` then `build`) that installs the backend's dependencies, runs `pytest`, and — only if tests pass — builds the Docker image.

**Verified, not just generated:** built and ran the image locally against the real backend code:
```
$ docker build -f phase1/task4/artifacts/Dockerfile -t task-manager-api phase1/task1/backend
$ docker run -d -p 8010:8000 task-manager-api
$ curl -X POST http://localhost:8010/tasks -d '{"title":"Docker smoke test"}'
$ curl -X PUT http://localhost:8010/tasks/<id> -d '{"status":"in-progress"}'
{"id":"...","title":"Docker smoke test","description":"","status":"in-progress","created_at":"..."}
```
Both requests succeeded inside the container, confirming the Dockerfile actually serves the feature, not just that it builds.
