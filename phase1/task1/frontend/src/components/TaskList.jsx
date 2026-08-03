import TaskItem from "./TaskItem.jsx";

export default function TaskList({ tasks, onUpdateStatus, onDelete }) {
  if (tasks.length === 0) {
    return <p className="empty">No tasks yet. Add one above.</p>;
  }

  return (
    <ul className="task-list">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onUpdateStatus={onUpdateStatus}
          onDelete={onDelete}
        />
      ))}
    </ul>
  );
}
