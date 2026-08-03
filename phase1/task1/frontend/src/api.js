const BASE_URL = "http://localhost:8000";

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    throw new Error(`Request failed: ${res.status}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

export const getTasks = () => request("/tasks");

export const createTask = (task) =>
  request("/tasks", { method: "POST", body: JSON.stringify(task) });

export const updateTaskStatus = (id, status) =>
  request(`/tasks/${id}`, { method: "PUT", body: JSON.stringify({ status }) });

export const deleteTask = (id) => request(`/tasks/${id}`, { method: "DELETE" });
