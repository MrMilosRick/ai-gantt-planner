# Roadmap to Production

This document separates the current MVP from the work needed before the product can be used in production. The MVP intentionally keeps state in memory and focuses on the end-to-end workflow: Gantt chart, Excel import/export, chat command, controlled tool execution, and immediate UI update.

## Data Persistence

- Add PostgreSQL as the primary database.
- Add schema migrations for all persisted entities.
- Introduce projects or workspaces so multiple plans can exist independently.
- Persist tasks, dependencies, imports, exports, and agent actions.
- Store plan snapshots or revisions to support history and rollback.

## Authentication and Access Control

- Add users and session management.
- Define roles such as owner, editor, viewer, and admin.
- Enforce project-level and workspace-level permissions.
- Restrict which data the agent can read or modify based on the current user.
- Add server-side authorization checks for all API endpoints and agent tools.

## Scheduling and Validation

- Detect dependency cycles before applying changes.
- Reject impossible or inconsistent schedules with clear errors.
- Support manual start and finish dates.
- Add milestones as first-class plan items.
- Support working calendars with weekends and holidays.
- Calculate critical path for schedule risk analysis.
- Add basic assignee workload and capacity checks.

## Agent Safety

- Require confirmation for destructive or broad changes.
- Add preview-before-apply for agent-generated actions.
- Keep an audit log of user requests, LLM outputs, tool calls, and final state changes.
- Support rollback to previous plan versions.
- Add automated tests for every tool action.
- Restrict available tools by user role and project permissions.
- Validate LLM JSON strictly before executing any action.

## Excel Import and Export

- Enforce a strict import template and version it.
- Return clear validation errors with row and column references.
- Add import preview before replacing the current plan.
- Process large files through background jobs.
- Support additional fields such as status, progress, dates, priority, and task type.

## Frontend UX

- Improve the Gantt chart with zooming, dependency lines, drag interactions, and better date scales.
- Add consistent loading, empty, and error states.
- Support inline task editing.
- Add undo and redo for user and agent changes.
- Add filters by assignee, date range, status, and search text.
- Improve responsive behavior for smaller screens.

## Testing

- Add backend unit tests for state transitions and scheduling.
- Add Excel import/export tests with valid and invalid templates.
- Add agent command tests for JSON validation and tool execution.
- Add frontend component tests for the Gantt chart, chat panel, upload, export, and modal behavior.
- Add an end-to-end test covering the main demo scenario.

## Operations and Deployment

- Add Docker images for backend and frontend.
- Add CI for linting, type checks, tests, and builds.
- Create separate staging and production environments.
- Add structured logging.
- Add tracing for API requests and agent actions.
- Add error reporting.
- Monitor LLM usage, latency, cost, and failure rates.
- Add rate limits for API and chat endpoints.
- Add health checks for the app, database, and background workers.
