import { startTransition, useState } from "react";

import { AgentActivityPage } from "./pages/AgentActivityPage";
import { AgentsOrgPage } from "./pages/AgentsOrgPage";
import { EmailOperationsPage } from "./pages/EmailOperationsPage";
import { InboxCalendarPage } from "./pages/InboxCalendarPage";
import { KnowledgeQnaPage } from "./pages/KnowledgeQnaPage";
import { ProposalGenerationPage } from "./pages/ProposalGenerationPage";
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
    description: "Review pending decisions and resolve them from the UI.",
  },
  {
    id: "agent-activity",
    label: "Agent Activity",
    description: "Inspect registered agents, runtime states, and deployment policies.",
  },
  {
    id: "agents-org",
    label: "Agents Org",
    description: "See corporate and delivery agents as an operating roster.",
  },
  {
    id: "inbox-calendar",
    label: "Inbox and Calendar",
    description: "Read live Outlook context and launch reply workflows from real messages.",
  },
  {
    id: "email-operations",
    label: "Email Operations",
    description: "Trigger the email workflow and feed the approval queue.",
  },
  {
    id: "knowledge-qna",
    label: "Knowledge Q&A",
    description: "Run grounded internal Q&A against the knowledge store.",
  },
  {
    id: "proposal-generation",
    label: "Proposal Generation",
    description: "Create a baseline consulting proposal from opportunity context.",
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
          {activeView === "agent-activity" ? (
            <AgentActivityPage refreshToken={refreshToken} />
          ) : null}
          {activeView === "agents-org" ? <AgentsOrgPage refreshToken={refreshToken} /> : null}
          {activeView === "inbox-calendar" ? (
            <InboxCalendarPage
              refreshToken={refreshToken}
              onDrafted={() => setRefreshToken((value) => value + 1)}
            />
          ) : null}
          {activeView === "email-operations" ? (
            <EmailOperationsPage onCreated={() => setRefreshToken((value) => value + 1)} />
          ) : null}
          {activeView === "knowledge-qna" ? <KnowledgeQnaPage /> : null}
          {activeView === "proposal-generation" ? <ProposalGenerationPage /> : null}
        </div>
      </main>
    </div>
  );
}
