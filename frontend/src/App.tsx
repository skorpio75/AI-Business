import { startTransition, useState } from "react";

import { ApprovalQueuePage } from "./pages/ApprovalQueuePage";
import { WorkflowMonitorPage } from "./pages/WorkflowMonitorPage";
import type { ViewKey } from "./types";

const VIEWS: Array<{ id: ViewKey; label: string; description: string }> = [
  {
    id: "workflow-monitor",
    label: "Workflow Monitor",
    description: "Track workflow throughput, model routing, and escalations.",
  },
  {
    id: "approval-queue",
    label: "Approval Queue",
    description: "Review pending decisions before action wiring lands.",
  },
];

export default function App() {
  const [activeView, setActiveView] = useState<ViewKey>("workflow-monitor");
  const [refreshToken, setRefreshToken] = useState(0);

  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <p className="eyebrow">Enterprise Agent Platform</p>
          <h1>Mission Control</h1>
        </div>
        <button
          className="refresh-button"
          type="button"
          onClick={() => setRefreshToken((value) => value + 1)}
        >
          Refresh data
        </button>
      </header>

      <main className="app-main">
        <aside className="nav-panel">
          <div className="nav-panel__intro">
            <p className="eyebrow">Operator views</p>
            <h2>Control surface</h2>
            <p>
              Phase 3 starts with a compact operator shell for live workflow visibility and CEO
              approval review.
            </p>
          </div>
          <nav className="view-nav" aria-label="Mission control views">
            {VIEWS.map((view) => (
              <button
                key={view.id}
                className={`view-nav__item ${activeView === view.id ? "view-nav__item--active" : ""}`}
                type="button"
                onClick={() =>
                  startTransition(() => {
                    setActiveView(view.id);
                  })
                }
              >
                <strong>{view.label}</strong>
                <span>{view.description}</span>
              </button>
            ))}
          </nav>
          <div className="nav-panel__footer">
            <span>API base</span>
            <code>{import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"}</code>
          </div>
        </aside>

        <div className="view-panel">
          {activeView === "workflow-monitor" ? (
            <WorkflowMonitorPage refreshToken={refreshToken} />
          ) : null}
          {activeView === "approval-queue" ? (
            <ApprovalQueuePage refreshToken={refreshToken} />
          ) : null}
        </div>
      </main>
    </div>
  );
}
