import React from 'react';
import { Download, Upload } from "lucide-react";
import { exportUrl } from "../api.js";

export default function Toolbar({ onUpload, busy }) {
  return (
    <header className="toolbar">
      <div>
        <h1>AI-планировщик Гантта</h1>
        <p>Тестовый план с импортом Excel, правками через чат и экспортом.</p>
      </div>
      <div className="toolbar-actions">
        <label className="button">
          <Upload size={18} />
          <span>Импорт Excel</span>
          <input
            type="file"
            accept=".xlsx,.xls"
            disabled={busy}
            onChange={(event) => {
              const file = event.target.files?.[0];
              if (file) onUpload(file);
              event.target.value = "";
            }}
          />
        </label>
        <a className="button secondary" href={exportUrl()}>
          <Download size={18} />
          <span>Экспорт Excel</span>
        </a>
      </div>
    </header>
  );
}
