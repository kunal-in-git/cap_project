import { useEffect, useState } from "react";
import TaskForm from "./components/TaskForm.jsx";
import TaskList from "./components/TaskList.jsx";
import { getTasks, createTask, updateTaskStatus, deleteTask } from "./api.js";

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [error, setError] = useState(null);

  const loadTasks = () => {
    getTasks()
      .then(setTasks)
      .catch((err) => setError(err.message));
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const handleCreate = async (task) => {
    try {
      await createTask(task);
      loadTasks();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleUpdateStatus = async (id, status) => {
    try {
      await updateTaskStatus(id, status);
      loadTasks();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteTask(id);
      loadTasks();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="app">
      <h1>Task Manager</h1>
      {error && <p className="error">{error}</p>}
      <TaskForm onCreate={handleCreate} />
      <TaskList
        tasks={tasks}
        onUpdateStatus={handleUpdateStatus}
        onDelete={handleDelete}
      />
    </div>
  );
}
