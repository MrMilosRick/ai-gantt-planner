import React from 'react';
import { X } from "lucide-react";

export default function TaskModal({ task, onClose }) {
  return (
    <div className="modal-backdrop" onClick={onClose}>
      <section className="modal" onClick={(event) => event.stopPropagation()}>
        <button className="icon-button" onClick={onClose} aria-label="Закрыть детали задачи">
          <X size={18} />
        </button>
        <h2 className="modal-title">{task.task}</h2>
        <dl className="task-details">
          <dt>ID</dt>
          <dd>{task.id}</dd>
          <dt>Описание</dt>
          <dd>{task.description || "Нет описания"}</dd>
          <dt>Исполнитель</dt>
          <dd>{task.assignee || "Не назначен"}</dd>
          <dt>Длительность</dt>
          <dd>{task.duration} дн.</dd>
          <dt>Даты</dt>
          <dd>
            {task.start} - {task.end}
          </dd>
          <dt>Предшественники</dt>
          <dd>{task.predecessors.length ? task.predecessors.join(", ") : "Нет"}</dd>
        </dl>
      </section>
    </div>
  );
}
