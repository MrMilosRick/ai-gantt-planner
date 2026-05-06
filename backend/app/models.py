from __future__ import annotations

from datetime import date
from typing import Any

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: str
    task: str
    description: str = ""
    assignee: str = ""
    duration: int = Field(default=1, ge=1)
    predecessors: list[str] = Field(default_factory=list)
    start: date | None = None
    end: date | None = None


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    actions: list[dict[str, Any]]
    tasks: list[Task]
