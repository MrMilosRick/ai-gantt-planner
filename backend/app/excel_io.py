from __future__ import annotations

from io import BytesIO
from typing import Iterable

import pandas as pd

from .models import Task

REQUIRED_COLUMNS = ["task", "description", "assignee", "duration", "predecessors"]


def tasks_from_excel(content: bytes) -> list[Task]:
    frame = pd.read_excel(BytesIO(content))
    missing = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    tasks: list[Task] = []
    for index, row in frame.iterrows():
        task_id = str(row.get("id") or f"T{index + 1}")
        predecessors = _parse_predecessors(row.get("predecessors"))
        duration = int(row.get("duration") or 1)
        tasks.append(
            Task(
                id=task_id,
                task=str(row.get("task") or "").strip(),
                description=str(row.get("description") or "").strip(),
                assignee=str(row.get("assignee") or "").strip(),
                duration=max(duration, 1),
                predecessors=predecessors,
            )
        )
    return tasks


def tasks_to_excel(tasks: Iterable[Task]) -> bytes:
    rows = [
        {
            "id": task.id,
            "task": task.task,
            "description": task.description,
            "assignee": task.assignee,
            "duration": task.duration,
            "predecessors": ", ".join(task.predecessors),
            "start": task.start.isoformat() if task.start else "",
            "end": task.end.isoformat() if task.end else "",
        }
        for task in tasks
    ]
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        pd.DataFrame(rows).to_excel(writer, index=False, sheet_name="Tasks")
    return output.getvalue()


def _parse_predecessors(value: object) -> list[str]:
    if value is None or pd.isna(value):
        return []
    return [item.strip() for item in str(value).split(",") if item.strip()]
