const STATUS_ORDER = ["todo", "in-progress", "done"];

function nextStatus(status) {
  const idx = STATUS_ORDER.indexOf(status);
  return STATUS_ORDER[(idx + 1) % STATUS_ORDER.length];
}

export default function TaskItem({ task, onUpdateStatus, onDelete }) {
  return (
    <li className={`task-item status-${task.status}`}>
      <div className="task-info">
        <h3>{task.title}</h3>
        {task.description && <p>{task.description}</p>}
        <span className="badge">{task.status}</span>
      </div>
      <div className="task-actions">
        <button onClick={() => onUpdateStatus(task.id, nextStatus(task.status))}>
          Advance Status
        </button>
        <button onClick={() => onDelete(task.id)} className="danger">
          Delete
        </button>
      </div>
    </li>
  );
}
