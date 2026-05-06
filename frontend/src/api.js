const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export async function fetchTasks() {
  const response = await fetch(`${API_BASE}/api/tasks`);
  return parseResponse(response);
}

export async function uploadTasks(file) {
  const form = new FormData();
  form.append("file", file);
  const response = await fetch(`${API_BASE}/api/tasks/upload`, {
    method: "POST",
    body: form,
  });
  return parseResponse(response);
}

export async function sendChat(message) {
  const response = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  return parseResponse(response);
}

export function exportUrl() {
  return `${API_BASE}/api/tasks/export`;
}

async function parseResponse(response) {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(error.detail || "Request failed");
  }
  return response.json();
}
