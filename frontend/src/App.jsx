import React from 'react';
import { useEffect, useState } from "react";
import { fetchTasks, sendChat, uploadTasks } from "./api.js";
import ChatPanel from "./components/ChatPanel.jsx";
import GanttView from "./components/GanttView.jsx";
import TaskModal from "./components/TaskModal.jsx";
import Toolbar from "./components/Toolbar.jsx";

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [selectedTask, setSelectedTask] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    fetchTasks().then(setTasks).catch((err) => setError(err.message));
  }, []);

  async function handleUpload(file) {
    setBusy(true);
    setError("");
    try {
      setTasks(await uploadTasks(file));
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function handleChat(message) {
    setBusy(true);
    setError("");
    try {
      const result = await sendChat(message);
      setTasks(result.tasks);
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="app-shell">
      <section className="workspace">
        <Toolbar onUpload={handleUpload} busy={busy} />
        {error ? <div className="error">{error}</div> : null}
        <GanttView tasks={tasks} onSelectTask={setSelectedTask} />
      </section>
      <ChatPanel onSend={handleChat} busy={busy} />
      {selectedTask ? <TaskModal task={selectedTask} onClose={() => setSelectedTask(null)} /> : null}
    </main>
  );
}
