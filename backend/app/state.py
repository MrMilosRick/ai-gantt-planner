from __future__ import annotations

from datetime import date, timedelta

from .models import Task
from .seed import seeded_tasks


class PlanState:
    def __init__(self) -> None:
        self._tasks: list[Task] = self._schedule(seeded_tasks())

    def list_tasks(self) -> list[Task]:
        return [task.model_copy(deep=True) for task in self._tasks]

    def replace_tasks(self, tasks: list[Task]) -> list[Task]:
        self._tasks = self._schedule(tasks)
        return self.list_tasks()

    def add_task(self, task: Task) -> list[Task]:
        self._tasks.append(task)
        self._tasks = self._schedule(self._tasks)
        return self.list_tasks()

    def update_task(self, task_id: str, updates: dict) -> list[Task]:
        for idx, task in enumerate(self._tasks):
            if task.id == task_id:
                data = task.model_dump()
                data.update({key: value for key, value in updates.items() if value is not None})
                self._tasks[idx] = Task(**data)
                break
        self._tasks = self._schedule(self._tasks)
        return self.list_tasks()

    def move_task(self, task_id: str, after_task_id: str | None = None) -> list[Task]:
        task = next((item for item in self._tasks if item.id == task_id), None)
        if not task:
            return self.list_tasks()

        remaining = [item for item in self._tasks if item.id != task_id]
        if after_task_id is None:
            self._tasks = [task, *remaining]
        else:
            insert_at = next(
                (idx + 1 for idx, item in enumerate(remaining) if item.id == after_task_id),
                len(remaining),
            )
            remaining.insert(insert_at, task)
            self._tasks = remaining

        self._tasks = self._schedule(self._tasks)
        return self.list_tasks()

    def set_dependencies(self, task_id: str, predecessors: list[str]) -> list[Task]:
        return self.update_task(task_id, {"predecessors": predecessors})

    def next_id(self) -> str:
        existing = {
            int(task.id[1:])
            for task in self._tasks
            if task.id.startswith("T") and task.id[1:].isdigit()
        }
        next_number = 1
        while next_number in existing:
            next_number += 1
        return f"T{next_number}"

    def _schedule(self, tasks: list[Task]) -> list[Task]:
        base = date.today()
        scheduled: list[Task] = []
        by_id: dict[str, Task] = {}

        for index, original in enumerate(tasks):
            task = original.model_copy(deep=True)
            predecessor_ends = [
                by_id[pred].end
                for pred in task.predecessors
                if pred in by_id and by_id[pred].end is not None
            ]
            if predecessor_ends:
                start = max(predecessor_ends) + timedelta(days=1)
            elif scheduled:
                start = scheduled[-1].end + timedelta(days=1) if scheduled[-1].end else base
            else:
                start = base + timedelta(days=index)

            task.start = start
            task.end = start + timedelta(days=task.duration - 1)
            scheduled.append(task)
            by_id[task.id] = task

        return scheduled


plan_state = PlanState()
