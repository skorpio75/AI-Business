/* Copyright (c) Dario Pizzolante */
import { useEffect, useState } from "react";

import { StatusPill } from "../components/StatusPill";
import { apiClient } from "../lib/api";
import type { AgentContract } from "../types";

type AgentsOrgPageProps = {
  refreshToken: number;
};

const DOMAIN_ORDER: Array<AgentContract["domain"]> = ["corporate", "delivery", "platform"];

function initialsFor(name: string): string {
  return name
    .split(/\s+/)
    .map((part) => part[0]?.toUpperCase() ?? "")
    .join("")
    .slice(0, 2);
}

export function AgentsOrgPage({ refreshToken }: AgentsOrgPageProps) {
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
          <p className="eyebrow">Agents org</p>
          <h2>See the corporate and delivery roster as an operating organization.</h2>
        </div>
        <p className="hero-copy">
          This view groups agents by domain and gives each role a quick visual identity, approval
          posture, and runtime status.
        </p>
      </div>

      {loading ? <p className="panel-state">Loading agents org view...</p> : null}
      {error ? <p className="panel-state panel-state--error">{error}</p> : null}

      <div className="org-grid">
        {DOMAIN_ORDER.map((domain) => {
          const domainAgents = agents.filter((agent) => agent.domain === domain);
          return (
            <section key={domain} className="panel">
              <div className="panel-header">
                <div className="list-card__topline">
                  <p className="eyebrow">{domain}</p>
                  <strong>{domainAgents.length} agents</strong>
                </div>
                <h3>{domain === "platform" ? "Platform counsel" : `${domain} function`}</h3>
              </div>
              <div className="org-lane">
                {domainAgents.map((agent) => (
                  <article key={agent.agent_id} className="org-card">
                    <div className="org-card__header">
                      <div className="avatar-chip">{initialsFor(agent.display_name)}</div>
                      <div>
                        <strong>{agent.display_name}</strong>
                        <p>{agent.role_summary}</p>
                      </div>
                    </div>
                    <div className="org-card__meta">
                      <StatusPill label={agent.runtime.status} tone={agent.runtime.status === "disabled" ? "critical" : "success"} />
                      <StatusPill label={agent.approval_class.replace("_", " ")} tone="neutral" />
                    </div>
                  </article>
                ))}
              </div>
            </section>
          );
        })}
      </div>
    </section>
  );
}
