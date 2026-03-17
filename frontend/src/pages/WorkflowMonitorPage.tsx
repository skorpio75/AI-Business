/* Copyright (c) Dario Pizzolante */
import { useEffect, useMemo, useState } from "react";

import { ModelRouteIndicator } from "../components/ModelRouteIndicator";
import { StatusPill } from "../components/StatusPill";
import { apiClient } from "../lib/api";
import { formatConfidence, truncate } from "../lib/format";
import type {
  AgentRunRecord,
  AuditEventRecord,
  DashboardSummary,
  WorkflowRun,
  WorkflowTrace,
} from "../types";

function runStatusTone(run: WorkflowRun): "neutral" | "success" | "warning" | "critical" {
  if (run.status === "completed" && run.approval_status === "approved") {
    return run.send_status === "sent" ? "success" : "neutral";
  }
  if (run.status === "completed" && run.approval_status === "rejected") {
    return "critical";
  }
  return "warning";
}

function traceSignalTone(value: string | null | undefined): "neutral" | "success" | "warning" | "critical" {
  if (!value) {
    return "neutral";
  }
  const normalized = value.toLowerCase();
  if (
    normalized.includes("fail") ||
    normalized.includes("reject") ||
    normalized.includes("block") ||
    normalized.includes("critical")
  ) {
    return "critical";
  }
  if (
    normalized.includes("escalat") ||
    normalized.includes("pending") ||
    normalized.includes("warn") ||
    normalized.includes("fallback")
  ) {
    return "warning";
  }
  if (normalized.includes("complete") || normalized.includes("approve") || normalized.includes("sent")) {
    return "success";
  }
  return "neutral";
}

function prettyLabel(value: string | null | undefined): string {
  if (!value) {
    return "Not recorded";
  }
  return value.replace(/[._-]+/g, " ");
}

function formatTimestamp(value: string | null | undefined): string {
  if (!value) {
    return "Not recorded";
  }
  return new Date(value).toLocaleString();
}

function inlinePayloadSummary(payload: Record<string, unknown> | string | null | undefined): string | null {
  if (!payload) {
    return null;
  }
  if (typeof payload === "string") {
    return payload;
  }
  const entries = Object.entries(payload).slice(0, 3);
  if (!entries.length) {
    return null;
  }
  return entries.map(([key, value]) => `${prettyLabel(key)}=${String(value)}`).join(" · ");
}

function routeHops(trace: WorkflowTrace | null): string[] {
  if (!trace) {
    return [];
  }
  return Array.from(
    new Set(
      [...trace.agent_runs.map((run) => run.routing_path), ...trace.audit_events.map((event) => event.routing_path)].filter(
        (value): value is string => Boolean(value),
      ),
    ),
  );
}

function sourceEvents(trace: WorkflowTrace | null): string[] {
  if (!trace) {
    return [];
  }
  return Array.from(
    new Set(
      trace.agent_runs
        .map((run) => run.trigger_event_name)
        .filter((value): value is string => Boolean(value)),
    ),
  );
}

function traceEscalations(trace: WorkflowTrace | null, run: WorkflowRun | null): string[] {
  const signals = new Set<string>();
  if (run?.escalation_reason) {
    signals.add(run.escalation_reason);
  }
  if (!trace) {
    return Array.from(signals);
  }
  trace.agent_runs.forEach((item) => {
    if (item.status === "failed" || item.status === "blocked") {
      signals.add(`${item.agent_id}: ${prettyLabel(item.status)}`);
    }
    if (item.error_code) {
      signals.add(`${item.agent_id}: ${item.error_code}`);
    }
  });
  trace.audit_events.forEach((event) => {
    if (
      event.status === "failed" ||
      event.status === "blocked" ||
      event.status === "rejected" ||
      event.status === "escalated" ||
      event.event_name.includes("escalated")
    ) {
      signals.add(`${prettyLabel(event.event_name)} (${prettyLabel(event.status)})`);
    }
  });
  return Array.from(signals);
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
  const [selectedTrace, setSelectedTrace] = useState<WorkflowTrace | null>(null);
  const [traceLoading, setTraceLoading] = useState(false);
  const [traceError, setTraceError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    async function loadRuns() {
      setLoading(true);
      setError(null);

      try {
        const [nextRuns, nextSummary] = await Promise.all([apiClient.getWorkflowRuns(), apiClient.getDashboardSummary()]);
        if (!active) {
          return;
        }

        const orderedRuns = [...nextRuns].reverse();
        setRuns(orderedRuns);
        setSummary(nextSummary);
        setSelectedWorkflowId((current) => {
          if (current && orderedRuns.some((run) => run.workflow_id === current)) {
            return current;
          }
          return orderedRuns[0]?.workflow_id ?? null;
        });
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

  useEffect(() => {
    let active = true;

    async function loadTrace(workflowId: string) {
      setTraceLoading(true);
      setTraceError(null);
      try {
        const trace = await apiClient.getWorkflowTrace(workflowId);
        if (!active) {
          return;
        }
        setSelectedTrace(trace);
      } catch (loadError) {
        if (!active) {
          return;
        }
        setSelectedTrace(null);
        setTraceError(loadError instanceof Error ? loadError.message : "unknown_error");
      } finally {
        if (active) {
          setTraceLoading(false);
        }
      }
    }

    if (!selectedWorkflowId) {
      setSelectedTrace(null);
      setTraceError(null);
      setTraceLoading(false);
      return () => {
        active = false;
      };
    }

    void loadTrace(selectedWorkflowId);
    return () => {
      active = false;
    };
  }, [selectedWorkflowId, refreshToken]);

  const selectedRun =
    runs.find((run) => run.workflow_id === selectedWorkflowId) ?? runs[0] ?? null;
  const escalationCount = runs.filter((run) => run.escalation_reason).length;
  const averageConfidence = runs.length
    ? Math.round((runs.reduce((sum, run) => sum + run.confidence, 0) / runs.length) * 100)
    : 0;

  const traceRouteSummary = useMemo(() => routeHops(selectedTrace), [selectedTrace]);
  const traceSourceSummary = useMemo(() => sourceEvents(selectedTrace), [selectedTrace]);
  const traceEscalationSummary = useMemo(
    () => traceEscalations(selectedTrace, selectedRun),
    [selectedRun, selectedTrace],
  );
  const selectedAuditEvents = selectedTrace?.audit_events ?? [];
  const selectedAgentRuns = selectedTrace?.agent_runs ?? [];

  return (
    <section className="page-grid">
      <div className="hero-card">
        <div>
          <p className="eyebrow">Workflow monitor</p>
          <h2>Track live approval-bound runs from the API.</h2>
        </div>
        <p className="hero-copy">
          This page reads `GET /workflows/runs` and `GET /audit/workflows/{'{'}workflow_id{'}'}` so
          Mission Control can show source events, routing paths, and escalation visibility without
          leaving the dashboard.
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
        <article className="stat-card">
          <span>Trace events</span>
          <strong>{selectedAuditEvents.length}</strong>
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
                  <StatusPill
                    label={`${run.status.replace("_", " ")} / ${run.approval_status}`}
                    tone={runStatusTone(run)}
                  />
                  <span>{formatConfidence(run.confidence)}</span>
                </div>
                <h4>{run.intent}</h4>
                <p>{truncate(run.draft_reply, 118)}</p>
                <ModelRouteIndicator
                  providerUsed={run.provider_used}
                  modelUsed={run.model_used}
                  localLlmInvoked={run.local_llm_invoked}
                  cloudLlmInvoked={run.cloud_llm_invoked}
                  llmDiagnosticCode={run.llm_diagnostic_code}
                  llmDiagnosticDetail={run.llm_diagnostic_detail}
                  compact
                />
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
                <StatusPill
                  label={`${selectedRun.status.replace("_", " ")} / ${selectedRun.approval_status}`}
                  tone={runStatusTone(selectedRun)}
                />
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
                <span>Source provider</span>
                <strong>{selectedRun.source_provider ?? "Manual / not recorded"}</strong>
              </div>
              <div className="detail-row">
                <span>Local LLM</span>
                <StatusPill
                  label={selectedRun.local_llm_invoked ? "invoked" : "not invoked"}
                  tone={selectedRun.local_llm_invoked ? "success" : "neutral"}
                />
              </div>
              <div className="detail-row">
                <span>Confidence</span>
                <strong>{formatConfidence(selectedRun.confidence)}</strong>
              </div>
              <ModelRouteIndicator
                providerUsed={selectedRun.provider_used}
                modelUsed={selectedRun.model_used}
                localLlmInvoked={selectedRun.local_llm_invoked}
                cloudLlmInvoked={selectedRun.cloud_llm_invoked}
                llmDiagnosticCode={selectedRun.llm_diagnostic_code}
                llmDiagnosticDetail={selectedRun.llm_diagnostic_detail}
              />
              <section className="trace-section">
                <div className="trace-summary-grid">
                  <article className="list-card">
                    <div className="list-card__topline">
                      <p className="eyebrow">Source event</p>
                      <StatusPill
                        label={traceSourceSummary.length ? `${traceSourceSummary.length} tracked` : "pending"}
                        tone={traceSourceSummary.length ? "success" : "neutral"}
                      />
                    </div>
                    <p>{traceSourceSummary[0] ? prettyLabel(traceSourceSummary[0]) : "No source event recorded yet."}</p>
                  </article>
                  <article className="list-card">
                    <div className="list-card__topline">
                      <p className="eyebrow">Routing path</p>
                      <StatusPill
                        label={traceRouteSummary.length ? `${traceRouteSummary.length} hops` : "pending"}
                        tone={traceRouteSummary.length ? "warning" : "neutral"}
                      />
                    </div>
                    <p>{traceRouteSummary.length ? traceRouteSummary.join(" -> ") : "No routing path recorded yet."}</p>
                  </article>
                  <article className="list-card">
                    <div className="list-card__topline">
                      <p className="eyebrow">Escalation signals</p>
                      <StatusPill
                        label={`${traceEscalationSummary.length}`}
                        tone={traceEscalationSummary.length ? "warning" : "success"}
                      />
                    </div>
                    <p>
                      {traceEscalationSummary[0] ??
                        "No escalation or blocked signal is currently recorded for this run."}
                    </p>
                  </article>
                </div>
              </section>
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

              <section className="trace-section">
                <div className="panel-header">
                  <div>
                    <p className="eyebrow">Agent runs</p>
                    <h3>Execution chain</h3>
                  </div>
                  <StatusPill
                    label={traceLoading ? "loading" : `${selectedAgentRuns.length} runs`}
                    tone={traceLoading ? "warning" : "neutral"}
                  />
                </div>
                {traceError ? <p className="panel-state panel-state--error">{traceError}</p> : null}
                {!traceLoading && !traceError && !selectedAgentRuns.length ? (
                  <p className="panel-state">No agent runs recorded for this workflow yet.</p>
                ) : null}
                <div className="trace-list">
                  {selectedAgentRuns.map((agentRun: AgentRunRecord) => (
                    <article key={agentRun.agent_run_id} className="trace-card">
                      <div className="trace-card__header">
                        <div>
                          <p className="eyebrow">{prettyLabel(agentRun.mode)}</p>
                          <h4>{prettyLabel(agentRun.agent_id)}</h4>
                        </div>
                        <StatusPill label={prettyLabel(agentRun.status)} tone={traceSignalTone(agentRun.status)} />
                      </div>
                      <div className="trace-card__meta">
                        <span>{formatTimestamp(agentRun.started_at)}</span>
                        <span>{agentRun.routing_path ?? agentRun.provider_used ?? "path not recorded"}</span>
                      </div>
                      <p>
                        Source event: {prettyLabel(agentRun.trigger_event_name)}. Confidence:{" "}
                        {agentRun.confidence != null ? formatConfidence(agentRun.confidence) : "not scored"}.
                      </p>
                      {agentRun.error_code ? (
                        <p className="trace-card__error">
                          {agentRun.error_code}: {agentRun.error_detail ?? "No extra detail recorded."}
                        </p>
                      ) : null}
                    </article>
                  ))}
                </div>
              </section>

              <section className="trace-section">
                <div className="panel-header">
                  <div>
                    <p className="eyebrow">Audit timeline</p>
                    <h3>Trace events</h3>
                  </div>
                  <StatusPill
                    label={traceLoading ? "loading" : `${selectedAuditEvents.length} events`}
                    tone={traceLoading ? "warning" : "neutral"}
                  />
                </div>
                {traceError ? <p className="panel-state panel-state--error">{traceError}</p> : null}
                {!traceLoading && !traceError && !selectedAuditEvents.length ? (
                  <p className="panel-state">No audit events recorded for this workflow yet.</p>
                ) : null}
                <div className="trace-list">
                  {selectedAuditEvents.map((event: AuditEventRecord) => (
                    <article key={event.audit_event_id} className="trace-card">
                      <div className="trace-card__header">
                        <div>
                          <p className="eyebrow">{formatTimestamp(event.occurred_at)}</p>
                          <h4>{prettyLabel(event.event_name)}</h4>
                        </div>
                        <StatusPill label={prettyLabel(event.status)} tone={traceSignalTone(event.status)} />
                      </div>
                      <div className="trace-card__meta">
                        <span>{prettyLabel(event.actor_type)}: {prettyLabel(event.actor_id)}</span>
                        <span>{event.routing_path ?? event.provider_used ?? "path not recorded"}</span>
                      </div>
                      <p>
                        Entity: {prettyLabel(event.entity_type)} / {event.entity_id}
                        {event.step_id ? ` · Step ${event.step_id}` : ""}
                        {event.tool_id ? ` · Tool ${event.tool_id}` : ""}
                      </p>
                      {inlinePayloadSummary(event.payload_ref_or_inline) ? (
                        <p>{inlinePayloadSummary(event.payload_ref_or_inline)}</p>
                      ) : null}
                      {event.error_code ? (
                        <p className="trace-card__error">
                          {event.error_code}: {event.error_detail ?? "No extra detail recorded."}
                        </p>
                      ) : null}
                    </article>
                  ))}
                </div>
              </section>
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
                    <StatusPill
                      label={item.urgency}
                      tone={
                        item.urgency === "high"
                          ? "critical"
                          : item.urgency === "medium"
                            ? "warning"
                            : "success"
                      }
                    />
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
                      <StatusPill
                        label={item.severity}
                        tone={
                          item.severity === "critical"
                            ? "critical"
                            : item.severity === "warning"
                              ? "warning"
                              : "neutral"
                        }
                      />
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
