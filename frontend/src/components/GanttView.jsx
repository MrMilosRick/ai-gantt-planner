import React from 'react';
const TASK_COLUMN_WIDTH = 260;
const DAY_WIDTH = 44;

export default function GanttView({ tasks, onSelectTask }) {
  const dates = tasks.flatMap((task) => [new Date(task.start), new Date(task.end)]);
  const minDate = dates.length ? new Date(Math.min(...dates)) : new Date();
  const maxDate = dates.length ? new Date(Math.max(...dates)) : new Date();
  const totalDays = Math.max(daysBetween(minDate, maxDate) + 1, 1);
  const gridColumns = `${TASK_COLUMN_WIDTH}px repeat(${totalDays}, ${DAY_WIDTH}px)`;

  return (
    <div className="gantt">
      <div className="gantt-header" style={{ gridTemplateColumns: gridColumns }}>
        <div className="task-column">Задача</div>
        {Array.from({ length: totalDays }, (_, index) => {
          const date = addDays(minDate, index);
          return (
            <div className="day" key={date.toISOString()}>
              {date.toLocaleDateString(undefined, { month: "short", day: "numeric" })}
            </div>
          );
        })}
      </div>
      {tasks.map((task) => {
        const offset = daysBetween(minDate, new Date(task.start));
        return (
          <button
            className="gantt-row"
            key={task.id}
            style={{ gridTemplateColumns: gridColumns }}
            onClick={() => onSelectTask(task)}
          >
            <span className="task-name">
              <span className="task-title-line">
                <strong>{task.id}</strong>
                {task.task}
              </span>
              <span className="task-meta">Исполнитель: {task.assignee || "Не назначен"}</span>
            </span>
            {Array.from({ length: totalDays }, (_, index) => (
              <span className="gantt-cell" key={`${task.id}-${index}`} />
            ))}
            <span
              className="bar"
              title={`${task.assignee || "Не назначен"}: ${task.start} - ${task.end}, ${task.duration} дн.`}
              style={{
                gridColumn: `${offset + 2} / span ${task.duration}`,
              }}
            >
              {task.duration} дн.
            </span>
          </button>
        );
      })}
    </div>
  );
}

function daysBetween(start, end) {
  const ms = Date.UTC(end.getFullYear(), end.getMonth(), end.getDate()) - Date.UTC(start.getFullYear(), start.getMonth(), start.getDate());
  return Math.round(ms / 86400000);
}

function addDays(date, days) {
  const next = new Date(date);
  next.setDate(next.getDate() + days);
  return next;
}
