from __future__ import annotations

import json
import os
import re
from typing import Any

from openai import OpenAI
from dotenv import load_dotenv

from .mcp_tools import TOOL_SCHEMA, PlanTools
from .models import ChatResponse, Task
from .state import PlanState

load_dotenv()


class PlannerAgent:
    def __init__(self, state: PlanState) -> None:
        self.state = state
        self.tools = PlanTools(state)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else None

    def handle_message(self, message: str) -> ChatResponse:
        actions = self._actions_from_llm(message) if self.client else self._fallback_actions(message)
        tasks: list[Task] = self.state.list_tasks()
        applied: list[dict[str, Any]] = []

        for action in actions:
            tasks = self.tools.run(action)
            applied.append(action)

        reply = "Applied requested plan change." if applied else "No plan change was needed."
        if applied and applied[-1].get("tool") == "list_tasks":
            reply = f"There are {len(tasks)} tasks in the current plan."
        return ChatResponse(reply=reply, actions=applied, tasks=tasks)

    def _actions_from_llm(self, message: str) -> list[dict[str, Any]]:
        current_tasks = [task.model_dump(mode="json") for task in self.state.list_tasks()]
        system = (
            "You convert user planning requests into structured JSON tool actions. "
            "Return only a JSON array. Do not explain. "
            f"Available tools: {json.dumps(TOOL_SCHEMA)}"
        )
        response = self.client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": json.dumps({"tasks": current_tasks, "request": message})},
            ],
            temperature=0,
        )
        content = response.choices[0].message.content or "[]"
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            return []
        return _normalize_actions(parsed)

    def _fallback_actions(self, message: str) -> list[dict[str, Any]]:
        text = message.strip()
        lower = text.lower()

        if "list" in lower or "show" in lower or "покажи задачи" in lower or "список задач" in lower:
            return [{"tool": "list_tasks", "args": {}}]

        if lower.startswith("добавь задачу") or lower.startswith("добавить задачу"):
            duration = _extract_duration(lower)
            title = re.sub(r"^добав(?:ь|ить)\s+задачу\s+", "", text, flags=re.IGNORECASE)
            title = re.sub(r"\s+на\s+\d+\s+д(?:ень|ня|ней).*$", "", title, flags=re.IGNORECASE).strip()
            return [{"tool": "add_task", "args": {"task": title or "Новая задача", "duration": duration}}]

        if lower.startswith("add"):
            duration = _extract_duration(lower)
            title = re.sub(r"^add\s+", "", text, flags=re.IGNORECASE)
            title = re.sub(r"\s+for\s+\d+\s+days?.*$", "", title, flags=re.IGNORECASE).strip()
            return [{"tool": "add_task", "args": {"task": title or "New task", "duration": duration}}]

        if "длительность" in lower or lower.startswith("сделай"):
            task_id = _extract_task_id(text)
            duration = _extract_duration(lower)
            if task_id:
                return [{"tool": "update_task", "args": {"id": task_id, "duration": duration}}]

        if "duration" in lower:
            task_id = _extract_task_id(text)
            duration = _extract_duration(lower)
            if task_id:
                return [{"tool": "update_task", "args": {"id": task_id, "duration": duration}}]

        # TODO: Replace this fallback with mandatory LLM calls in production deployments.
        return []


def _extract_duration(text: str) -> int:
    match = re.search(r"(\d+)\s+(?:days?|день|дня|дней)", text)
    return int(match.group(1)) if match else 1


def _extract_task_id(text: str) -> str | None:
    match = re.search(r"\bT\d+\b", text, flags=re.IGNORECASE)
    return match.group(0).upper() if match else None


def _normalize_actions(raw: Any) -> list[dict[str, Any]]:
    if isinstance(raw, dict) and "actions" in raw:
        raw = raw["actions"]
    if not isinstance(raw, list):
        return []

    actions: list[dict[str, Any]] = []
    for action in raw:
        if not isinstance(action, dict) or "tool" not in action:
            continue

        normalized = dict(action)
        if "args" not in normalized and "arguments" in normalized:
            normalized["args"] = normalized.pop("arguments")
        if "args" not in normalized:
            normalized["args"] = {}
        if not isinstance(normalized["args"], dict):
            continue

        actions.append(normalized)
    return actions
