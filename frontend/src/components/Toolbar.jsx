import React from 'react';
import { Download, Upload } from "lucide-react";
import { exportUrl } from "../api.js";

export default function Toolbar({ onUpload, busy }) {
  return (
    <header className="toolbar">
      <div>
        <h1>AI Gantt Planner</h1>
        <p>Seeded MVP plan with Excel import, chat edits, and export.</p>
      </div>
      <div className="toolbar-actions">
        <label className="button">
          <Upload size={18} />
          <span>Import Excel</span>
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
          <span>Export Excel</span>
        </a>
      </div>
    </header>
  );
}
