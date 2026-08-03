# Task Manager — FastAPI + React

A simple full-stack task management app: FastAPI backend with in-memory storage, React (Vite) frontend.

## Features
- Create tasks with a title and description
- List all tasks with their status
- Advance a task's status (`todo` → `in-progress` → `done`)
- Delete tasks

## Project Structure
```
task1/
├── backend/
│   ├── main.py          # FastAPI app and routes
│   ├── models.py        # Pydantic Task model
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── package.json
    └── src/
        ├── App.jsx
        ├── api.js
        ├── index.css
        ├── main.jsx
        └── components/
            ├── TaskForm.jsx
            ├── TaskList.jsx
            └── TaskItem.jsx
```

## Backend — FastAPI

### Setup & Run
```bash
cd backend
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### Endpoints
| Method | Path          | Description                     |
|--------|---------------|----------------------------------|
| POST   | `/tasks`      | Create a new task                |
| GET    | `/tasks`      | List all tasks                   |
| PUT    | `/tasks/{id}` | Update a task's status           |
| DELETE | `/tasks/{id}` | Delete a task                    |

### Task model
```python
class Task(BaseModel):
    id: UUID
    title: str
    description: str = ""
    status: TaskStatus  # "todo" | "in-progress" | "done"
    created_at: datetime
```

## Frontend — React (Vite)

### Setup & Run
```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173` and talks to the backend at `http://localhost:8000` (CORS is enabled for this origin in `backend/main.py`).

## Running Both
Open two terminals — one for `backend` (`uvicorn main:app --reload --port 8000`) and one for `frontend` (`npm run dev`) — with the backend started first.

## AI-Generated Parts
This project was built with Claude (Anthropic). Claude generated:
- All 4 FastAPI endpoints (`POST /tasks`, `GET /tasks`, `PUT /tasks/{id}`, `DELETE /tasks/{id}`) in `backend/main.py`
- The Pydantic `Task` model in `backend/models.py`
- The full React frontend, including the `useState`/`useEffect` data-fetching logic in `App.jsx` and the `TaskForm`, `TaskList`, and `TaskItem` components

No parts were hand-written outside of AI generation; all code was reviewed for correctness before being committed.
