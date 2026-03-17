/* Copyright (c) Dario Pizzolante */
import { useEffect, useState } from "react";

import { StatusPill } from "../components/StatusPill";
import { apiClient } from "../lib/api";
import type { CloseChecklistItem, FinancePanel, FinancialScenario, ReconciliationException } from "../types";

type FinanceCockpitPageProps = {
  refreshToken: number;
};

function toneForException(
  severity: ReconciliationException["severity"],
): "warning" | "critical" {
  return severity === "warning" ? "warning" : "critical";
}

function toneForChecklist(
  status: CloseChecklistItem["status"],
): "neutral" | "warning" | "success" | "critical" {
  if (status === "completed") {
    return "success";
  }
  if (status === "in_progress") {
    return "warning";
  }
  if (status === "blocked") {
    return "critical";
  }
  return "neutral";
}

function toneForHorizon(
  horizon: FinancialScenario["horizon"],
): "neutral" | "warning" | "success" {
  if (horizon === "30_days") {
    return "warning";
  }
  if (horizon === "90_days") {
    return "success";
  }
  return "neutral";
}

export function FinanceCockpitPage({ refreshToken }: FinanceCockpitPageProps) {
  const [panel, setPanel] = useState<FinancePanel | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    async function loadPanel() {
      setLoading(true);
      setError(null);
      try {
        const nextPanel = await apiClient.getFinancePanel();
        if (!active) {
          return;
        }
        setPanel(nextPanel);
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

    void loadPanel();
    return () => {
      active = false;
    };
  }, [refreshToken]);

  return (
    <section className="page-grid">
      <div className="hero-card hero-card--amber">
        <div>
          <p className="eyebrow">Finance cockpit</p>
          <h2>Keep accounting exceptions, close status, and CFO decisions in one view.</h2>
        </div>
        <p className="hero-copy">
          This page reads `GET /specialists/finance/panel` and combines Accountant, Finance Ops,
          and CFO signals into one operator cockpit.
        </p>
      </div>

      {loading ? <p className="panel-state">Loading finance cockpit...</p> : null}
      {error ? <p className="panel-state panel-state--error">{error}</p> : null}

      {panel ? (
        <>
          <div className="stats-grid">
            <article className="stat-card">
              <span>Accounting exceptions</span>
              <strong>{panel.accounting_exceptions.length}</strong>
            </article>
            <article className="stat-card">
              <span>Close checklist items</span>
              <strong>{panel.close_checklist.length}</strong>
            </article>
            <article className="stat-card">
              <span>CFO scenarios</span>
              <strong>{panel.scenarios.length}</strong>
            </article>
          </div>

          <div className="dashboard-grid dashboard-grid--advisory">
            <section className="panel">
              <div className="panel-header">
                <div className="list-card__topline">
                  <StatusPill
                    label={panel.approval_required ? "approval required" : "advisory only"}
                    tone={panel.approval_required ? "warning" : "success"}
                  />
                  <StatusPill label="internal finance" tone="neutral" />
                </div>
                <div>
                  <p className="eyebrow">Executive summary</p>
                  <h3>Finance decision pack</h3>
                </div>
              </div>
              <div className="callout callout--soft">
                <strong>{panel.executive_summary}</strong>
              </div>

              <div className="assistant-section">
                <p className="eyebrow">Finance specialist roster</p>
                <div className="stack-list">
                  {panel.agents.map((agent) => (
                    <article key={agent.agent_id} className="list-card">
                      <div className="list-card__topline">
                        <strong>{agent.display_name}</strong>
                        <div className="tag-cloud">
                          <StatusPill label={agent.governed_metadata.routing_posture} tone="neutral" />
                          <StatusPill label={agent.governed_metadata.autonomy_label} tone="success" />
                        </div>
                      </div>
                      <p>{agent.role_summary}</p>
                      <span className="muted-note">{agent.governed_metadata.operating_model_label}</span>
                      <span className="muted-note">{agent.governed_metadata.routing_posture_label}</span>
                    </article>
                  ))}
                </div>
              </div>

              <div className="mini-list">
                <p className="eyebrow">Accounting-ready exports</p>
                <ul>
                  {panel.accounting_ready_exports.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            </section>

            <section className="panel panel--detail">
              <div className="panel-header">
                <div>
                  <p className="eyebrow">Accounting control</p>
                  <h3>Exceptions and close readiness</h3>
                </div>
              </div>
              <div className="mini-list">
                <p className="eyebrow">Reconciliation rules</p>
                <ul>
                  {panel.reconciliation_rules.map((rule) => (
                    <li key={rule.rule_id}>
                      <strong>{rule.severity}</strong>: {rule.description}
                    </li>
                  ))}
                </ul>
              </div>
              <div className="assistant-section">
                <p className="eyebrow">Exceptions</p>
                <div className="stack-list">
                  {panel.accounting_exceptions.map((item) => (
                    <article key={item.exception_id} className="list-card">
                      <div className="list-card__topline">
                        <strong>{item.summary}</strong>
                        <StatusPill label={item.severity} tone={toneForException(item.severity)} />
                      </div>
                      <div className="mini-list">
                        <p className="eyebrow">Impacted records</p>
                        <ul>
                          {item.impacted_records.map((record) => (
                            <li key={record}>{record}</li>
                          ))}
                        </ul>
                      </div>
                      <div className="callout callout--soft">
                        <p className="eyebrow">Recommended action</p>
                        <strong>{item.recommended_action}</strong>
                      </div>
                    </article>
                  ))}
                </div>
              </div>
              <div className="assistant-section">
                <p className="eyebrow">Close checklist</p>
                <div className="stack-list">
                  {panel.close_checklist.map((item) => (
                    <article key={item.item_id} className="list-card">
                      <div className="list-card__topline">
                        <strong>{item.title}</strong>
                        <StatusPill label={item.status.replaceAll("_", " ")} tone={toneForChecklist(item.status)} />
                      </div>
                      <p>Owner: {item.owner}</p>
                      {item.notes ? <span className="muted-note">{item.notes}</span> : null}
                    </article>
                  ))}
                </div>
              </div>
            </section>

            <section className="panel panel--detail">
              <div className="panel-header">
                <div>
                  <p className="eyebrow">CFO scenarios</p>
                  <h3>Cashflow and decision cards</h3>
                </div>
              </div>
              <div className="assistant-section">
                <p className="eyebrow">Scenario cards</p>
                <div className="stack-list">
                  {panel.scenarios.map((scenario) => (
                    <article key={scenario.scenario_id} className="list-card">
                      <div className="list-card__topline">
                        <strong>{scenario.title}</strong>
                        <StatusPill label={scenario.horizon.replace("_", " ")} tone={toneForHorizon(scenario.horizon)} />
                      </div>
                      <div className="mini-list">
                        <p className="eyebrow">Assumptions</p>
                        <ul>
                          {scenario.assumptions.map((item) => (
                            <li key={item}>{item}</li>
                          ))}
                        </ul>
                      </div>
                      <div className="mini-list">
                        <p className="eyebrow">Projected outcomes</p>
                        <ul>
                          {scenario.projected_outcomes.map((item) => (
                            <li key={item}>{item}</li>
                          ))}
                        </ul>
                      </div>
                      <div className="mini-list">
                        <p className="eyebrow">Risks</p>
                        <ul>
                          {scenario.risks.map((item) => (
                            <li key={item}>{item}</li>
                          ))}
                        </ul>
                      </div>
                    </article>
                  ))}
                </div>
              </div>
              <div className="mini-list">
                <p className="eyebrow">Cashflow risks</p>
                <ul>
                  {panel.cashflow_risks.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
              <div className="mini-list">
                <p className="eyebrow">Recommendations</p>
                <ul>
                  {panel.recommendations.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            </section>
          </div>
        </>
      ) : null}
    </section>
  );
}
