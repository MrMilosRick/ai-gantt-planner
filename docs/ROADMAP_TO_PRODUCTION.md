# Roadmap to Production

## Near Term

- Replace in-memory state with persistent storage and migrations.
- Require authenticated users and per-workspace plan isolation.
- Add validation for dependency cycles, invalid task IDs, and impossible schedules.
- Expand chat tools with confirmations for destructive or broad changes.
- Add automated tests for scheduling, Excel import/export, and chat tool execution.

## Product Depth

- Add manual date overrides, milestones, progress, and critical path views.
- Add basic resource availability only after the MVP workflow is validated.
- Add version history and plan snapshots.
- Add collaborative editing and conflict handling.

## Operations

- Add structured logging, request tracing, and error reporting.
- Add deployment configuration after the local MVP is accepted.
- Add CI for backend and frontend checks.
- Add rate limits and LLM usage monitoring.
