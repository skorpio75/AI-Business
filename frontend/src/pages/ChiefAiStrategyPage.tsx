/* Copyright (c) Dario Pizzolante */
import { useEffect, useState } from "react";

import { ModelRouteIndicator } from "../components/ModelRouteIndicator";
import { StatusPill } from "../components/StatusPill";
import { apiClient } from "../lib/api";
import type { ChiefAIPanel, DeliveryBlueprintPhase, MaturityDimension, OpportunityMapItem } from "../types";

type ChiefAiStrategyPageProps = {
  refreshToken: number;
};

function toneForPriority(priority: OpportunityMapItem["priority"]): "critical" | "warning" | "neutral" {
  if (priority === "now") {
    return "critical";
  }
  if (priority === "next") {
    return "warning";
  }
  return "neutral";
}

function toneForMaturity(
  level: MaturityDimension["current_level"],
): "neutral" | "warning" | "success" {
  if (level === "managed" || level === "optimized") {
    return "success";
  }
  if (level === "repeatable") {
    return "warning";
  }
  return "neutral";
}

function toneForBlueprintRisk(phase: DeliveryBlueprintPhase): "warning" | "success" {
  return phase.risks.length ? "warning" : "success";
}

export function ChiefAiStrategyPage({ refreshToken }: ChiefAiStrategyPageProps) {
  const [panel, setPanel] = useState<ChiefAIPanel | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    async function loadPanel() {
      setLoading(true);
      setError(null);
      try {
        const nextPanel = await apiClient.getChiefAiPanel();
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
          <p className="eyebrow">Chief AI / Digital Strategy</p>
          <h2>Map AI opportunities, delivery roadmaps, and maturity gaps in one place.</h2>
        </div>
        <p className="hero-copy">
          This page reads `GET /specialists/chief-ai-digital-strategy/panel` and packages AI
          opportunity design, delivery blueprinting, and maturity signals into a specialist
          strategy surface.
        </p>
      </div>

      {loading ? <p className="panel-state">Loading Chief AI / Digital Strategy panel...</p> : null}
      {error ? <p className="panel-state panel-state--error">{error}</p> : null}

      {panel ? (
        <>
          <div className="stats-grid">
            <article className="stat-card">
              <span>AI opportunities</span>
              <strong>{panel.opportunity_map.length}</strong>
            </article>
            <article className="stat-card">
              <span>Blueprint phases</span>
              <strong>{panel.delivery_blueprint.length}</strong>
            </article>
            <article className="stat-card">
              <span>Maturity dimensions</span>
              <strong>{panel.maturity_model.length}</strong>
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
                <p className="eyebrow">Executive summary</p>
                <strong>{panel.executive_summary}</strong>
              </div>

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
                <p className="eyebrow">Scope signals</p>
                <div className="stack-list">
                  {panel.scope_signals.map((signal) => (
                    <article key={signal.signal_id} className="list-card">
                      <div className="list-card__topline">
                        <strong>{signal.title}</strong>
                        <StatusPill label={signal.tone} tone={signal.tone} />
                      </div>
                      <p>{signal.summary}</p>
                      <span className="muted-note">{signal.focus_area.replace("_", " ")}</span>
                    </article>
                  ))}
                </div>
              </div>
            </section>

            <section className="panel panel--detail">
              <div className="panel-header">
                <div>
                  <p className="eyebrow">Opportunity portfolio</p>
                  <h3>Priority AI opportunities</h3>
                </div>
              </div>
              <div className="stack-list">
                {panel.opportunity_map.map((item) => (
                  <article key={item.opportunity_id} className="list-card">
                    <div className="list-card__topline">
                      <strong>{item.title}</strong>
                      <StatusPill label={item.priority} tone={toneForPriority(item.priority)} />
                    </div>
                    <div className="mini-list">
                      <p className="eyebrow">Problem statement</p>
                      <ul>
                        <li>{item.problem_statement}</li>
                      </ul>
                    </div>
                    <div className="callout callout--soft">
                      <p className="eyebrow">Expected value</p>
                      <strong>{item.expected_value}</strong>
                    </div>
                    <div className="mini-list">
                      <p className="eyebrow">Dependencies</p>
                      <ul>
                        {item.dependencies.map((dependency) => (
                          <li key={dependency}>{dependency}</li>
                        ))}
                      </ul>
                    </div>
                  </article>
                ))}
              </div>
            </section>

            <section className="panel panel--detail">
              <div className="panel-header">
                <div>
                  <p className="eyebrow">Delivery blueprint</p>
                  <h3>AI/data roadmap phases</h3>
                </div>
              </div>
              <div className="stack-list">
                {panel.delivery_blueprint.map((phase) => (
                  <article key={phase.phase_id} className="list-card">
                    <div className="list-card__topline">
                      <strong>{phase.title}</strong>
                      <StatusPill label={phase.risks.length ? "risk noted" : "ready"} tone={toneForBlueprintRisk(phase)} />
                    </div>
                    <div className="mini-list">
                      <p className="eyebrow">Objectives</p>
                      <ul>
                        {phase.objectives.map((item) => (
                          <li key={item}>{item}</li>
                        ))}
                      </ul>
                    </div>
                    <div className="mini-list">
                      <p className="eyebrow">Deliverables</p>
                      <ul>
                        {phase.deliverables.map((item) => (
                          <li key={item}>{item}</li>
                        ))}
                      </ul>
                    </div>
                    <div className="mini-list">
                      <p className="eyebrow">Risks</p>
                      <ul>
                        {phase.risks.map((item) => (
                          <li key={item}>{item}</li>
                        ))}
                      </ul>
                    </div>
                  </article>
                ))}
              </div>
            </section>
          </div>

          <section className="panel">
            <div className="panel-header">
              <div>
                <p className="eyebrow">Maturity model</p>
                <h3>Capability gaps and next actions</h3>
              </div>
            </div>
            <div className="stack-list">
              {panel.maturity_model.map((dimension) => (
                <article key={dimension.dimension} className="list-card">
                  <div className="list-card__topline">
                    <strong>{dimension.dimension}</strong>
                    <div className="tag-cloud">
                      <StatusPill label={`current ${dimension.current_level}`} tone={toneForMaturity(dimension.current_level)} />
                      <StatusPill label={`target ${dimension.target_level}`} tone="success" />
                    </div>
                  </div>
                  <p>{dimension.gap_summary}</p>
                  <div className="mini-list">
                    <p className="eyebrow">Next actions</p>
                    <ul>
                      {dimension.next_actions.map((item) => (
                        <li key={item}>{item}</li>
                      ))}
                    </ul>
                  </div>
                </article>
              ))}
            </div>
          </section>
        </>
      ) : null}
    </section>
  );
}
