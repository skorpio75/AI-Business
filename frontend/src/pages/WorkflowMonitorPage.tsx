import { useEffect, useState } from "react";

import { StatusPill } from "../components/StatusPill";
import { apiClient } from "../lib/api";
import { formatConfidence, truncate } from "../lib/format";
import type { WorkflowRun } from "../types";

type WorkflowMonitorPageProps = {
  refreshToken: number;
};

export function WorkflowMonitorPage({ refreshToken }: WorkflowMonitorPageProps) {
  const [runs, setRuns] = useState<WorkflowRun[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedWorkflowId, setSelectedWorkflowId] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    async function loadRuns() {
      setLoading(true);
      setError(null);

      try {
        const nextRuns = await apiClient.getWorkflowRuns();
        if (!active) {
          return;
        }

        const orderedRuns = [...nextRuns].reverse();
        setRuns(orderedRuns);
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

      <div className="content-grid">
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
                  <StatusPill label={run.status.replace("_", " ")} tone="warning" />
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
                <StatusPill label="pending approval" tone="warning" />
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
      </div>
    </section>
  );
}
