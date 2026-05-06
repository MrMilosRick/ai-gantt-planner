import React from 'react';
import { X } from "lucide-react";

export default function TaskModal({ task, onClose }) {
  return (
    <div className="modal-backdrop" onClick={onClose}>
      <section className="modal" onClick={(event) => event.stopPropagation()}>
        <button className="icon-button" onClick={onClose} aria-label="Close task details">
          <X size={18} />
        </button>
        <h2>{task.task}</h2>
        <dl>
          <dt>ID</dt>
          <dd>{task.id}</dd>
          <dt>Description</dt>
          <dd>{task.description || "No description"}</dd>
          <dt>Assignee</dt>
          <dd>{task.assignee || "Unassigned"}</dd>
          <dt>Duration</dt>
          <dd>{task.duration} day(s)</dd>
          <dt>Dates</dt>
          <dd>
            {task.start} to {task.end}
          </dd>
          <dt>Predecessors</dt>
          <dd>{task.predecessors.length ? task.predecessors.join(", ") : "None"}</dd>
        </dl>
      </section>
    </div>
  );
}
