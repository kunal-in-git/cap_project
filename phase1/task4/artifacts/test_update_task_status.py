"""
Test artifact for the "Update Task Status" feature, written for
Task D (AI-Gated SDLC Flow Document). Targets the real app in
../../task1/backend without modifying that folder.

Run from phase1/task4/artifacts with the task1 backend's venv active:
    pytest test_update_task_status.py
"""
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "task1" / "backend"))

import main  # noqa: E402


@pytest.fixture
def client():
    main.tasks.clear()
    return TestClient(main.app)


def create_task(client, title="Write SDLC doc"):
    resp = client.post("/tasks", json={"title": title, "description": "desc"})
    assert resp.status_code == 201
    return resp.json()


# --- AI-suggested cases -----------------------------------------------

def test_update_status_to_in_progress(client):
    task = create_task(client)
    resp = client.put(f"/tasks/{task['id']}", json={"status": "in-progress"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "in-progress"


def test_update_status_to_done(client):
    task = create_task(client)
    resp = client.put(f"/tasks/{task['id']}", json={"status": "done"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "done"


def test_update_status_persists_in_list(client):
    task = create_task(client)
    client.put(f"/tasks/{task['id']}", json={"status": "done"})
    resp = client.get("/tasks")
    assert resp.json()[0]["status"] == "done"


def test_update_status_unknown_task_returns_404(client):
    resp = client.put(
        "/tasks/00000000-0000-0000-0000-000000000000", json={"status": "done"}
    )
    assert resp.status_code == 404


def test_update_status_invalid_enum_value_returns_422(client):
    task = create_task(client)
    resp = client.put(f"/tasks/{task['id']}", json={"status": "cancelled"})
    assert resp.status_code == 422


# --- Edge cases the AI's first pass missed -----------------------------

def test_update_status_malformed_id_returns_422_not_404(client):
    # Claude's first test list assumed a bad id would 404 like an unknown
    # id. It doesn't: a non-UUID path param fails FastAPI's param parsing
    # before the route body even runs, so it's a 422, not a 404.
    resp = client.put("/tasks/not-a-uuid", json={"status": "done"})
    assert resp.status_code == 422


def test_update_status_is_idempotent(client):
    # Not in the original suggestions: repeating the same update should
    # be safe and return the same result, not error or toggle anything.
    task = create_task(client)
    first = client.put(f"/tasks/{task['id']}", json={"status": "done"})
    second = client.put(f"/tasks/{task['id']}", json={"status": "done"})
    assert first.json()["status"] == second.json()["status"] == "done"


def test_update_status_can_move_backward(client):
    # The endpoint has no state machine guard, so "done" -> "todo" is
    # currently allowed. Worth flagging even though it's not a crash.
    task = create_task(client)
    client.put(f"/tasks/{task['id']}", json={"status": "done"})
    resp = client.put(f"/tasks/{task['id']}", json={"status": "todo"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "todo"
