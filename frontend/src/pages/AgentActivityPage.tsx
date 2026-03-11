import { useEffect, useState } from "react";

import { StatusPill } from "../components/StatusPill";
import { apiClient } from "../lib/api";
import type { AgentContract } from "../types";

type AgentActivityPageProps = {
  refreshToken: number;
};

export function AgentActivityPage({ refreshToken }: AgentActivityPageProps) {
  const [agents, setAgents] = useState<AgentContract[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    async function loadAgents() {
      setLoading(true);
      setError(null);
      try {
        const nextAgents = await apiClient.getAgents();
        if (!active) {
          return;
        }
        setAgents(nextAgents);
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

    void loadAgents();
    return () => {
      active = false;
    };
  }, [refreshToken]);

  return (
    <section className="page-grid">
      <div className="hero-card hero-card--mint">
        <div>
          <p className="eyebrow">Agent activity</p>
          <h2>Inspect the current internal operator roster.</h2>
        </div>
        <p className="hero-copy">
          This view reads `GET /agents` and surfaces roles, deployment policy, runtime status, and
          constraints before the org visualization lands in `P3-T09`.
        </p>
      </div>

      {loading ? <p className="panel-state">Loading agent registry...</p> : null}
      {error ? <p className="panel-state panel-state--error">{error}</p> : null}

      <div className="agent-grid">
        {agents.map((agent) => (
          <article key={agent.agent_id} className="panel agent-card">
            <div className="panel-header">
              <div className="list-card__topline">
                <StatusPill label={agent.runtime.status} tone="success" />
                <StatusPill label={agent.domain} tone="neutral" />
              </div>
              <div>
                <p className="eyebrow">{agent.agent_id}</p>
                <h3>{agent.display_name}</h3>
              </div>
            </div>

            <p>{agent.role_summary}</p>

            <div className="detail-stack">
              <div className="detail-row">
                <span>Approval class</span>
                <strong>{agent.approval_class.replace("_", " ")}</strong>
              </div>
              <div className="detail-row">
                <span>Primary track</span>
                <strong>{agent.deployment.primary_track.replaceAll("_", " ")}</strong>
              </div>
              <div className="detail-row">
                <span>Replication</span>
                <strong>{agent.deployment.replication_mode.replace("_", " ")}</strong>
              </div>
            </div>

            {agent.deployment.replication_notes ? (
              <div className="callout callout--soft">
                <p className="eyebrow">Deployment note</p>
                <strong>{agent.deployment.replication_notes}</strong>
              </div>
            ) : null}

            <div className="tag-cloud">
              {agent.capabilities.map((capability) => (
                <span key={capability.id} className="tag-chip">
                  {capability.name}
                </span>
              ))}
            </div>

            <div className="mini-list">
              <p className="eyebrow">Tools</p>
              <ul>
                {agent.tools.map((tool) => (
                  <li key={tool}>{tool}</li>
                ))}
              </ul>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
