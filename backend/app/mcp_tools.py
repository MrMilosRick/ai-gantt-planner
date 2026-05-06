from __future__ import annotations

from typing import Any

from .models import Task
from .state import PlanState


class PlanTools:
    """Controlled MCP-style tools that are the only way agent actions mutate state."""

    def __init__(self, state: PlanState) -> None:
        self.state = state

    def run(self, action: dict[str, Any]) -> list[Task]:
        name = action.get("tool")
        args = action.get("args", {})

        if name == "list_tasks":
            return self.state.list_tasks()
        if name == "add_task":
            task = Task(
                id=args.get("id") or self.state.next_id(),
                task=args["task"],
                description=args.get("description", ""),
                assignee=args.get("assignee", ""),
                duration=int(args.get("duration", 1)),
                predecessors=args.get("predecessors", []),
            )
            return self.state.add_task(task)
        if name == "update_task":
            task_id = args["id"]
            updates = {key: value for key, value in args.items() if key != "id"}
            return self.state.update_task(task_id, updates)
        if name == "move_task":
            return self.state.move_task(args["id"], args.get("after_task_id"))
        if name == "set_dependencies":
            return self.state.set_dependencies(args["id"], args.get("predecessors", []))

        raise ValueError(f"Unsupported tool: {name}")


TOOL_SCHEMA = [
    {
        "tool": "add_task",
        "args": {
            "task": "string",
            "description": "string",
            "assignee": "string",
            "duration": "integer",
            "predecessors": ["task id"],
        },
    },
    {"tool": "update_task", "args": {"id": "task id", "task": "string", "duration": "integer"}},
    {"tool": "move_task", "args": {"id": "task id", "after_task_id": "task id or null"}},
    {"tool": "set_dependencies", "args": {"id": "task id", "predecessors": ["task id"]}},
    {"tool": "list_tasks", "args": {}},
]
