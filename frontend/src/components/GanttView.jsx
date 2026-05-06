import React from 'react';
const DAY_WIDTH = 44;

export default function GanttView({ tasks, onSelectTask }) {
  const dates = tasks.flatMap((task) => [new Date(task.start), new Date(task.end)]);
  const minDate = dates.length ? new Date(Math.min(...dates)) : new Date();
  const maxDate = dates.length ? new Date(Math.max(...dates)) : new Date();
  const totalDays = Math.max(daysBetween(minDate, maxDate) + 1, 1);

  return (
    <div className="gantt">
      <div className="gantt-header" style={{ gridTemplateColumns: `220px repeat(${totalDays}, ${DAY_WIDTH}px)` }}>
        <div className="task-column">Task</div>
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
            style={{ gridTemplateColumns: `220px repeat(${totalDays}, ${DAY_WIDTH}px)` }}
            onClick={() => onSelectTask(task)}
          >
            <span className="task-name">
              <strong>{task.id}</strong>
              {task.task}
            </span>
            <span
              className="bar"
              style={{
                gridColumn: `${offset + 2} / span ${task.duration}`,
              }}
            >
              {task.assignee || "Unassigned"}
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
