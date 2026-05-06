from __future__ import annotations

from .models import Task


def seeded_tasks() -> list[Task]:
    return [
        Task(
            id="T1",
            task="Discovery",
            description="Clarify scope and acceptance criteria.",
            assignee="PM",
            duration=2,
            predecessors=[],
        ),
        Task(
            id="T2",
            task="Design MVP plan",
            description="Define milestones, task order, and risks.",
            assignee="Planner",
            duration=3,
            predecessors=["T1"],
        ),
        Task(
            id="T3",
            task="Build prototype",
            description="Implement the first working Gantt planner flow.",
            assignee="Engineer",
            duration=5,
            predecessors=["T2"],
        ),
        Task(
            id="T4",
            task="Review demo",
            description="Run the demo scenario and collect feedback.",
            assignee="Stakeholder",
            duration=1,
            predecessors=["T3"],
        ),
    ]
