# AI Gantt Planner MVP

Minimal full-stack skeleton for an AI-native Gantt planner test task.

## What Is Included

- React + Vite frontend with an interactive Gantt chart.
- FastAPI backend with seeded in-memory plan state.
- Excel import/export for `task`, `description`, `assignee`, `duration`, `predecessors`.
- Chat endpoint that asks an LLM for structured JSON actions when `OPENAI_API_KEY` is set.
- Controlled MCP-style tool layer in `backend/app/mcp_tools.py`.
- Fallback demo parser for a few simple chat commands when no API key is configured.

## Local Run

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## API

- `GET /api/health`
- `GET /api/tasks`
- `POST /api/tasks/upload`
- `GET /api/tasks/export`
- `POST /api/chat`

## Demo Scenario

1. Start the backend and frontend.
2. Open `http://localhost:5173` and confirm seeded tasks render in the Gantt chart.
3. Click a task bar to open the task details modal.
4. Upload `samples/sample_tasks.xlsx` using Import Excel.
5. Send a chat command such as `add QA review for 2 days`.
6. Confirm the new task appears immediately in the chart.
7. Export the current plan to Excel.

## MVP Boundaries

- No authentication.
- No database.
- No Docker.
- No complex resource planning.
- Current plan is stored in backend memory.
- Scheduling uses simple task order and predecessor-derived start dates.
