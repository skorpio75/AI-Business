import { useEffect, useState } from "react";

import { StatusPill } from "../components/StatusPill";
import { apiClient } from "../lib/api";
import { formatConfidence, truncate } from "../lib/format";
import type { DashboardSummary, WorkflowRun } from "../types";

function runStatusTone(run: WorkflowRun): "neutral" | "success" | "warning" | "critical" {
  if (run.status === "completed" && run.approval_status === "approved") {
    return run.send_status === "sent" ? "success" : "neutral";
  }
  if (run.status === "completed" && run.approval_status === "rejected") {
    return "critical";
  }
  return "warning";
}

type WorkflowMonitorPageProps = {
  refreshToken: number;
};

export function WorkflowMonitorPage({ refreshToken }: WorkflowMonitorPageProps) {
  const [runs, setRuns] = useState<WorkflowRun[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedWorkflowId, setSelectedWorkflowId] = useState<string | null>(null);
  const [summary, setSummary] = useState<DashboardSummary | null>(null);

  useEffect(() => {
    let active = true;

    async function loadRuns() {
      setLoading(true);
      setError(null);

      try {
        const [nextRuns, nextSummary] = await Promise.all([
          apiClient.getWorkflowRuns(),
          apiClient.getDashboardSummary(),
        ]);
        if (!active) {
          return;
        }

        const orderedRuns = [...nextRuns].reverse();
        setRuns(orderedRuns);
        setSummary(nextSummary);
        setSelectedWorkflowId((current) => current ?? orderedRuns[0]?.workflow_id ?? null);
      } catch (loadError) {
        if (!active) {
          return;
        }
        setError(loadError instanceof Error ? loadError.message : "unknown_error");
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    void loadRuns();
    return () => {
      active = false;
    };
  }, [refreshToken]);

  const selectedRun =
    runs.find((run) => run.workflow_id === selectedWorkflowId) ?? runs[0] ?? null;
  const escalationCount = runs.filter((run) => run.escalation_reason).length;
  const averageConfidence = runs.length
    ? Math.round((runs.reduce((sum, run) => sum + run.confidence, 0) / runs.length) * 100)
    : 0;

  return (
    <section className="page-grid">
      <div className="hero-card">
        <div>
          <p className="eyebrow">Workflow monitor</p>
          <h2>Track live approval-bound runs from the API.</h2>
        </div>
        <p className="hero-copy">
          This page reads `GET /workflows/runs` and surfaces the current queue shape, model
          choices, and escalation patterns.
        </p>
      </div>

      <div className="stats-grid">
        <article className="stat-card">
          <span>Total runs</span>
          <strong>{runs.length}</strong>
        </article>
        <article className="stat-card">
          <span>Average confidence</span>
          <strong>{averageConfidence}%</strong>
        </article>
        <article className="stat-card">
          <span>Escalations</span>
          <strong>{escalationCount}</strong>
        </article>
      </div>

      <div className="kpi-grid">
        {summary?.kpis.map((kpi) => (
          <article key={kpi.id} className={`panel kpi-card kpi-card--${kpi.tone}`}>
            <div className="list-card__topline">
              <p className="eyebrow">{kpi.label}</p>
              <StatusPill label={kpi.tone} tone={kpi.tone} />
            </div>
            <strong>{kpi.value}</strong>
            <p>{kpi.context}</p>
            {kpi.footnote ? <span className="muted-note">{kpi.footnote}</span> : null}
          </article>
        ))}
      </div>

      <div className="dashboard-grid">
        <section className="panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Run queue</p>
              <h3>Email workflow runs</h3>
            </div>
          </div>
          {loading ? <p className="panel-state">Loading workflow runs...</p> : null}
          {error ? <p className="panel-state panel-state--error">{error}</p> : null}
          {!loading && !error && runs.length === 0 ? (
            <p className="panel-state">No workflow runs yet.</p>
          ) : null}
          <div className="stack-list">
            {runs.map((run) => (
              <button
                key={run.workflow_id}
                className={`list-card ${selectedRun?.workflow_id === run.workflow_id ? "list-card--active" : ""}`}
                type="button"
                onClick={() => setSelectedWorkflowId(run.workflow_id)}
              >
                <div className="list-card__topline">
                  <StatusPill label={`${run.status.replace("_", " ")} / ${run.approval_status}`} tone={runStatusTone(run)} />
                  <span>{formatConfidence(run.confidence)}</span>
                </div>
                <h4>{run.intent}</h4>
                <p>{truncate(run.draft_reply, 118)}</p>
                <div className="list-card__meta">
                  <span>{run.provider_used}</span>
                  <span>{truncate(run.model_used, 28)}</span>
                </div>
              </button>
            ))}
          </div>
        </section>

        <aside className="panel panel--detail">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Selected run</p>
              <h3>{selectedRun?.intent ?? "No run selected"}</h3>
            </div>
          </div>
          {selectedRun ? (
            <div className="detail-stack">
              <div className="detail-row">
                <span>Workflow ID</span>
                <code>{selectedRun.workflow_id}</code>
              </div>
              <div className="detail-row">
                <span>Approval ID</span>
                <code>{selectedRun.approval_id}</code>
              </div>
              <div className="detail-row">
                <span>Status</span>
                <StatusPill label={`${selectedRun.status.replace("_", " ")} / ${selectedRun.approval_status}`} tone={runStatusTone(selectedRun)} />
              </div>
              <div className="detail-row">
                <span>Send</span>
                <strong>
                  {selectedRun.send_status}
                  {selectedRun.sent_at ? ` at ${new Date(selectedRun.sent_at).toLocaleString()}` : ""}
                </strong>
              </div>
              <div className="detail-row">
                <span>Model path</span>
                <strong>
                  {selectedRun.provider_used} / {selectedRun.model_used}
                </strong>
              </div>
              <div className="detail-row">
                <span>Confidence</span>
                <strong>{formatConfidence(selectedRun.confidence)}</strong>
              </div>
              <div className="draft-block">
                <p className="eyebrow">Draft reply</p>
                <pre>{selectedRun.draft_reply}</pre>
              </div>
              {selectedRun.escalation_reason ? (
                <div className="callout">
                  <p className="eyebrow">Escalation reason</p>
                  <strong>{selectedRun.escalation_reason}</strong>
                </div>
              ) : (
                <div className="callout callout--soft">
                  <p className="eyebrow">Escalation</p>
                  <strong>No escalation reason recorded for this run.</strong>
                </div>
              )}
            </div>
          ) : (
            <p className="panel-state">Select a workflow run to inspect it.</p>
          )}
        </aside>

        <aside className="panel panel--detail assistant-panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Personal assistant</p>
              <h3>Today brief</h3>
            </div>
            <div className="list-card__topline">
              <StatusPill label={`inbox ${summary?.personal_assistant.inbox_status ?? "unknown"}`} tone="neutral" />
              <StatusPill label={`calendar ${summary?.personal_assistant.calendar_status ?? "unknown"}`} tone="neutral" />
            </div>
          </div>
          <div className="assistant-section">
            <p className="eyebrow">Priorities</p>
            <div className="stack-list">
              {summary?.personal_assistant.priorities.map((item) => (
                <article key={item.title} className="list-card">
                  <div className="list-card__topline">
                    <strong>{item.title}</strong>
                    <StatusPill label={item.urgency} tone={item.urgency === "high" ? "critical" : item.urgency === "medium" ? "warning" : "success"} />
                  </div>
                  <p>{item.reason}</p>
                </article>
              ))}
            </div>
          </div>
          <div className="assistant-section">
            <p className="eyebrow">Schedule conflicts</p>
            <div className="stack-list">
              {summary?.personal_assistant.schedule_conflicts.length ? (
                summary.personal_assistant.schedule_conflicts.map((item) => (
                  <article key={item.title} className="list-card">
                    <div className="list-card__topline">
                      <strong>{item.title}</strong>
                      <StatusPill label={item.severity} tone={item.severity === "critical" ? "critical" : item.severity === "warning" ? "warning" : "neutral"} />
                    </div>
                    <p>{item.detail}</p>
                  </article>
                ))
              ) : (
                <p className="panel-state">No conflicts detected in the current assistant window.</p>
              )}
            </div>
          </div>
          <div className="assistant-section">
            <p className="eyebrow">Quick actions</p>
            <div className="tag-cloud">
              {summary?.personal_assistant.quick_actions.map((item) => (
                <span key={item.label} className="tag-chip">
                  {item.label}
                </span>
              ))}
            </div>
            <div className="mini-list">
              <ul>
                {summary?.personal_assistant.quick_actions.map((item) => (
                  <li key={`${item.label}-${item.target_view}`}>
                    <strong>{item.label}</strong>: {item.reason}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </aside>
      </div>
    </section>
  );
}
