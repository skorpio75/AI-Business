/* Copyright (c) Dario Pizzolante */
import { useEffect, useState } from "react";

import { ModelRouteIndicator } from "../components/ModelRouteIndicator";
import { StatusPill } from "../components/StatusPill";
import { apiClient } from "../lib/api";
import type { CTOCIOPanel } from "../types";

type CtoCioPageProps = {
  refreshToken: number;
};

function toneForPriority(priority: "now" | "next" | "later"): "critical" | "warning" | "neutral" {
  if (priority === "now") {
    return "critical";
  }
  if (priority === "next") {
    return "warning";
  }
  return "neutral";
}

function toneForImpact(impact: "low" | "medium" | "high"): "neutral" | "warning" | "success" {
  if (impact === "high") {
    return "success";
  }
  if (impact === "medium") {
    return "warning";
  }
  return "neutral";
}

export function CtoCioPage({ refreshToken }: CtoCioPageProps) {
  const [panel, setPanel] = useState<CTOCIOPanel | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    async function loadPanel() {
      setLoading(true);
      setError(null);
      try {
        const nextPanel = await apiClient.getCtoCioPanel();
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
      <div className="hero-card hero-card--mint">
        <div>
          <p className="eyebrow">CTO/CIO panel</p>
          <h2>Turn platform signals into technology strategy options.</h2>
        </div>
        <p className="hero-copy">
          This page reads `GET /specialists/cto-cio/panel` and packages customer-scope insight,
          architecture direction, and internal improvement priorities into one advisory surface.
        </p>
      </div>

      {loading ? <p className="panel-state">Loading CTO/CIO panel...</p> : null}
      {error ? <p className="panel-state panel-state--error">{error}</p> : null}

      {panel ? (
        <>
          <div className="stats-grid">
            <article className="stat-card">
              <span>Scope insights</span>
              <strong>{panel.scope_insights.length}</strong>
            </article>
            <article className="stat-card">
              <span>Strategy options</span>
              <strong>{panel.strategy_options.length}</strong>
            </article>
            <article className="stat-card">
              <span>Improvement backlog</span>
              <strong>{panel.internal_improvement_backlog.length}</strong>
            </article>
          </div>

          <div className="dashboard-grid dashboard-grid--advisory">
            <section className="panel">
              <div className="panel-header">
                <div className="list-card__topline">
                  <StatusPill label={panel.primary_track.replaceAll("_", " ")} tone="neutral" />
                  <StatusPill
                    label={panel.approval_required ? "approval required" : "advisory only"}
                    tone={panel.approval_required ? "warning" : "success"}
                  />
                </div>
                <div>
                  <p className="eyebrow">{panel.agent_id}</p>
                  <h3>{panel.display_name}</h3>
                </div>
              </div>
              <p>{panel.role_summary}</p>

              <div className="callout callout--soft">
                <p className="eyebrow">Operating modes</p>
                <strong>{panel.operating_modes.map((mode) => mode.replaceAll("_", " ")).join(", ")}</strong>
              </div>

              <div className="callout callout--soft">
                <p className="eyebrow">Model routing</p>
                <ModelRouteIndicator
                  providerUsed={panel.provider_used}
                  modelUsed={panel.model_used}
                  localLlmInvoked={panel.local_llm_invoked}
                  cloudLlmInvoked={panel.cloud_llm_invoked}
                  llmDiagnosticCode={panel.llm_diagnostic_code}
                  llmDiagnosticDetail={panel.llm_diagnostic_detail}
                />
              </div>

              {Object.keys(panel.tool_profile_by_mode).length > 0 ? (
                <div className="mini-list">
                  <p className="eyebrow">Tool profiles</p>
                  <ul>
                    {Object.entries(panel.tool_profile_by_mode).map(([mode, profileId]) => (
                      <li key={mode}>
                        <strong>{mode.replaceAll("_", " ")}</strong>: {profileId}
                      </li>
                    ))}
                  </ul>
                </div>
              ) : null}

              <div className="assistant-section">
                <p className="eyebrow">Customer scope insights</p>
                <div className="stack-list">
                  {panel.scope_insights.map((item) => (
                    <article key={item.insight_id} className="list-card">
                      <div className="list-card__topline">
                        <strong>{item.title}</strong>
                        <StatusPill label={item.tone} tone={item.tone} />
                      </div>
                      <p>{item.summary}</p>
                      <span className="muted-note">{item.focus_area.replace("_", " ")}</span>
                    </article>
                  ))}
                </div>
              </div>
            </section>

            <section className="panel panel--detail">
              <div className="panel-header">
                <div>
                  <p className="eyebrow">Strategy options</p>
                  <h3>Decision paths</h3>
                </div>
              </div>
              <div className="stack-list">
                {panel.strategy_options.map((option) => (
                  <article key={option.option_id} className="list-card">
                    <div className="list-card__topline">
                      <strong>{option.title}</strong>
                      <StatusPill label="option" tone="neutral" />
                    </div>
                    <p>{option.summary}</p>
                    <div className="mini-list">
                      <p className="eyebrow">Benefits</p>
                      <ul>
                        {option.benefits.map((item) => (
                          <li key={item}>{item}</li>
                        ))}
                      </ul>
                    </div>
                    <div className="mini-list">
                      <p className="eyebrow">Tradeoffs</p>
                      <ul>
                        {option.tradeoffs.map((item) => (
                          <li key={item}>{item}</li>
                        ))}
                      </ul>
                    </div>
                    <div className="callout callout--soft">
                      <p className="eyebrow">Recommended when</p>
                      <strong>{option.recommended_when}</strong>
                    </div>
                  </article>
                ))}
              </div>
            </section>

            <section className="panel panel--detail">
              <div className="panel-header">
                <div>
                  <p className="eyebrow">Architecture advice</p>
                  <h3>Current and target state</h3>
                </div>
              </div>
              <div className="detail-stack">
                <div className="callout callout--soft">
                  <p className="eyebrow">Current state</p>
                  <strong>{panel.architecture_advice.current_state}</strong>
                </div>
                <div className="callout callout--soft">
                  <p className="eyebrow">Target state</p>
                  <strong>{panel.architecture_advice.target_state}</strong>
                </div>
                <div className="mini-list">
                  <p className="eyebrow">Key constraints</p>
                  <ul>
                    {panel.architecture_advice.key_constraints.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </div>
                <div className="mini-list">
                  <p className="eyebrow">Proposed changes</p>
                  <ul>
                    {panel.architecture_advice.proposed_changes.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </div>
                <div className="mini-list">
                  <p className="eyebrow">Risks</p>
                  <ul>
                    {panel.architecture_advice.risks.map((item) => (
                      <li key={item}>{item}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </section>
          </div>

          <section className="panel">
            <div className="panel-header">
              <div>
                <p className="eyebrow">Internal improvement queue</p>
                <h3>Prioritized platform backlog</h3>
              </div>
            </div>
            <div className="stack-list">
              {panel.internal_improvement_backlog.map((item) => (
                <article key={item.item_id} className="list-card">
                  <div className="list-card__topline">
                    <strong>{item.title}</strong>
                    <div className="tag-cloud">
                      <StatusPill label={item.priority} tone={toneForPriority(item.priority)} />
                      <StatusPill label={`${item.impact} impact`} tone={toneForImpact(item.impact)} />
                      <StatusPill label={`${item.effort} effort`} tone="neutral" />
                    </div>
                  </div>
                  <p>{item.rationale}</p>
                  {item.owner_hint ? <span className="muted-note">Owner hint: {item.owner_hint}</span> : null}
                </article>
              ))}
            </div>
          </section>
        </>
      ) : null}
    </section>
  );
}
