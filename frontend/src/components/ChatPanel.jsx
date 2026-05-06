import React from 'react';
import { Send } from "lucide-react";
import { useState } from "react";

export default function ChatPanel({ onSend, busy }) {
  const [message, setMessage] = useState("");
  const [history, setHistory] = useState([
    { role: "assistant", text: "Попробуйте: добавь задачу Тестирование на 2 дня, покажи задачи, измени длительность T3 на 4 дня." },
  ]);

  async function submit(event) {
    event.preventDefault();
    const text = message.trim();
    if (!text) return;
    setMessage("");
    setHistory((items) => [...items, { role: "user", text }]);
    try {
      const response = await onSend(text);
      setHistory((items) => [...items, { role: "assistant", text: response.reply }]);
    } catch (err) {
      setHistory((items) => [...items, { role: "assistant", text: err.message }]);
    }
  }

  return (
    <aside className="chat-panel">
      <h2>Planner chat</h2>
      <div className="messages">
        {history.map((item, index) => (
          <div className={`message ${item.role}`} key={`${item.role}-${index}`}>
            {item.text}
          </div>
        ))}
      </div>
      <form className="chat-form" onSubmit={submit}>
        <input
          value={message}
          disabled={busy}
          onChange={(event) => setMessage(event.target.value)}
          placeholder="Попросите изменить план..."
        />
        <button type="submit" disabled={busy || !message.trim()} aria-label="Send message">
          <Send size={18} />
        </button>
      </form>
    </aside>
  );
}
