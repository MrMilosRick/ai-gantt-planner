# AI Gantt Planner MVP

AI Gantt Planner is a minimal full-stack prototype for editing a project plan through a web UI and an AI chat interface. It starts with seeded test data, renders an interactive Gantt chart, supports Excel import/export, and applies chat-driven plan changes through a controlled tools layer.

This is an MVP skeleton for a test task, not a Microsoft Project replacement. The goal is to demonstrate the end-to-end AI-native workflow with a small, readable codebase.

## User Flow

1. Open the React app at `http://localhost:5173`.
2. See a Gantt chart populated with seeded backend tasks.
3. Upload an Excel file with task data.
4. Ask the chat to change the plan, for example `add QA review for 2 days`.
5. See the updated plan immediately reflected on the Gantt chart.
6. Click a task bar to open the task details modal.
7. Export the current plan back to Excel.

## Stack

- Frontend: React and Vite.
- Backend: Python FastAPI.
- Excel: pandas and openpyxl.
- LLM: API-based chat completion when `OPENAI_API_KEY` is configured.
- Agent tools: MCP-style controlled action layer between the LLM and plan state.

## Project Structure

```text
backend/
  app/
    main.py        FastAPI app, CORS, API routes.
    models.py      Pydantic request, response, and task models.
    seed.py        Seeded MVP task data.
    state.py       In-memory plan state and simple scheduling logic.
    excel_io.py    Excel import/export helpers.
    agent.py       Chat orchestration, LLM JSON actions, fallback demo parser.
    mcp_tools.py   Controlled MCP-style tools that mutate the plan.
frontend/
  src/
    App.jsx        Main frontend state and API coordination.
    api.js         HTTP client helpers.
    components/    Gantt chart, chat panel, toolbar, and task modal.
samples/
  sample_tasks.xlsx
docs/
  ROADMAP_TO_PRODUCTION.md
```

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

To enable real LLM calls, set `OPENAI_API_KEY` in `backend/.env`. Without an API key, the backend uses a small fallback parser for simple demo commands.

## API Endpoints

- `GET /api/health` returns backend health status.
- `GET /api/tasks` returns the current scheduled task list.
- `POST /api/tasks/upload` imports tasks from an Excel file and replaces the current in-memory plan.
- `GET /api/tasks/export` exports the current plan as an Excel workbook.
- `POST /api/chat` accepts a natural-language planning command and returns updated tasks.

## Excel Format

Input Excel files must include these columns:

- `task`: task title.
- `description`: task description.
- `assignee`: responsible person or role.
- `duration`: task duration in days.
- `predecessors`: comma-separated predecessor task IDs, for example `T1, T2`.

The sample file is available at `samples/sample_tasks.xlsx`.

## Agent Flow

1. The user sends a planning command in chat.
2. The FastAPI backend receives the message at `POST /api/chat`.
3. If an API key is configured, the LLM returns structured JSON actions instead of free-form schedule edits.
4. The backend executes those actions only through MCP-style tools in `backend/app/mcp_tools.py`.
5. The backend returns the updated plan.
6. The frontend updates the Gantt chart immediately from the response.

Supported agent tools:

- `list_tasks`
- `add_task`
- `update_task`
- `move_task`
- `set_dependencies`

## Demo Scenario

1. Start the backend and frontend.
2. Open `http://localhost:5173` and confirm seeded tasks render in the Gantt chart.
3. Upload `samples/sample_tasks.xlsx` using Import Excel.
4. Send `add QA review for 2 days` in the chat.
5. Confirm the new task appears immediately in the chart.
6. Click a task to open its details modal.
7. Export the current plan to Excel.

## How AI Assistants Were Used

AI assistants were used to accelerate development, draft the project structure, check architectural options, prepare documentation, and look for implementation issues. Final decisions about MVP boundaries, architecture, verification, and delivery scope were made manually.

## MVP Boundaries

- No authentication.
- No database.
- No Docker.
- No complex resource planning.
- No working-day or holiday calendar.
- No critical path calculation.
- Current plan state is stored in backend memory.
- These are intentional MVP constraints to keep the prototype minimal and demonstrable.
