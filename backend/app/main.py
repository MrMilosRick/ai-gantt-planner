from __future__ import annotations

import os

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from .agent import PlannerAgent
from .excel_io import tasks_from_excel, tasks_to_excel
from .models import ChatRequest, ChatResponse, Task
from .state import plan_state

app = FastAPI(title="AI Gantt Planner MVP")

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://ai-gantt-planner-gcz5gi462-milosturbos-projects.vercel.app",
]
if os.getenv("FRONTEND_ORIGIN"):
    allowed_origins.append(os.getenv("FRONTEND_ORIGIN"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = PlannerAgent(plan_state)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/tasks", response_model=list[Task])
def get_tasks() -> list[Task]:
    return plan_state.list_tasks()


@app.post("/api/tasks/upload", response_model=list[Task])
async def upload_tasks(file: UploadFile = File(...)) -> list[Task]:
    try:
        content = await file.read()
        tasks = tasks_from_excel(content)
        return plan_state.replace_tasks(tasks)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/api/tasks/export")
def export_tasks() -> Response:
    content = tasks_to_excel(plan_state.list_tasks())
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="gantt_plan.xlsx"'},
    )


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        return agent.handle_message(request.message)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
