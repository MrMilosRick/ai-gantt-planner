from __future__ import annotations

from .models import Task


def seeded_tasks() -> list[Task]:
    return [
        Task(
            id="T1",
            task="Анализ требований",
            description="Уточнить цели, ограничения и критерии приемки.",
            assignee="Продакт",
            duration=2,
            predecessors=[],
        ),
        Task(
            id="T2",
            task="Планирование MVP",
            description="Определить этапы, порядок задач и основные риски.",
            assignee="Планировщик",
            duration=3,
            predecessors=["T1"],
        ),
        Task(
            id="T3",
            task="Разработка прототипа",
            description="Собрать первый рабочий сценарий планировщика Гантта.",
            assignee="Инженер",
            duration=5,
            predecessors=["T2"],
        ),
        Task(
            id="T4",
            task="Демо и обратная связь",
            description="Показать демо-сценарий и собрать замечания.",
            assignee="Заказчик",
            duration=1,
            predecessors=["T3"],
        ),
    ]
