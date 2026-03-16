/* Copyright (c) Dario Pizzolante */
import { useState } from "react";

import { ModelRouteIndicator } from "../components/ModelRouteIndicator";
import { StatusPill } from "../components/StatusPill";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Textarea } from "../components/ui/textarea";
import { apiClient } from "../lib/api";
import type { ProposalGenerationResponse } from "../types";

export function ProposalGenerationPage() {
  const [clientName, setClientName] = useState("");
  const [opportunitySummary, setOpportunitySummary] = useState("");
  const [desiredOutcomes, setDesiredOutcomes] = useState("");
  const [constraints, setConstraints] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ProposalGenerationResponse | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      const nextResult = await apiClient.runProposalGeneration({
        client_name: clientName,
        opportunity_summary: opportunitySummary,
        desired_outcomes: desiredOutcomes.split("\n").map((item) => item.trim()).filter(Boolean),
        constraints: constraints.split("\n").map((item) => item.trim()).filter(Boolean),
      });
      setResult(nextResult);
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "unknown_error");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="page-grid">
      <div className="hero-card hero-card--amber">
        <div>
          <p className="eyebrow">Proposal generation</p>
          <h2>Generate a baseline consulting proposal from an opportunity summary.</h2>
        </div>
        <p className="hero-copy">
          This page submits to `POST /workflows/proposal-generation/run` and returns a first-pass
          proposal draft for CEO review.
        </p>
      </div>

      <div className="content-grid">
        <form className="panel form-panel" onSubmit={handleSubmit}>
          <div className="panel-header">
            <div>
              <p className="eyebrow">Proposal input</p>
              <h3>Baseline draft builder</h3>
            </div>
          </div>
          <label className="form-field">
            <span>Client name</span>
            <Input value={clientName} onChange={(event) => setClientName(event.target.value)} required />
          </label>
          <label className="form-field">
            <span>Opportunity summary</span>
            <Textarea
              value={opportunitySummary}
              onChange={(event) => setOpportunitySummary(event.target.value)}
              rows={7}
              required
            />
          </label>
          <label className="form-field">
            <span>Desired outcomes (one per line)</span>
            <Textarea
              value={desiredOutcomes}
              onChange={(event) => setDesiredOutcomes(event.target.value)}
              rows={4}
            />
          </label>
          <label className="form-field">
            <span>Constraints (one per line)</span>
            <Textarea value={constraints} onChange={(event) => setConstraints(event.target.value)} rows={4} />
          </label>
          {error ? <p className="panel-state panel-state--error">{error}</p> : null}
          <Button className="refresh-button" type="submit" disabled={submitting}>
            {submitting ? "Generating..." : "Generate proposal"}
          </Button>
        </form>

        <aside className="panel panel--detail">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Proposal draft</p>
              <h3>{result?.title ?? "No proposal generated yet"}</h3>
            </div>
          </div>
          {result ? (
            <div className="detail-stack">
              <div className="detail-row">
                <span>Workflow ID</span>
                <code>{result.workflow_id}</code>
              </div>
              <div className="detail-row">
                <span>Model path</span>
                <strong>
                  {result.provider_used} / {result.model_used}
                </strong>
              </div>
              <div className="detail-row">
                <span>Local LLM</span>
                <StatusPill
                  label={result.local_llm_invoked ? "invoked" : "not invoked"}
                  tone={result.local_llm_invoked ? "success" : "neutral"}
                />
              </div>
              <ModelRouteIndicator
                providerUsed={result.provider_used}
                modelUsed={result.model_used}
                localLlmInvoked={result.local_llm_invoked}
                cloudLlmInvoked={result.cloud_llm_invoked}
                llmDiagnosticCode={result.llm_diagnostic_code}
                llmDiagnosticDetail={result.llm_diagnostic_detail}
              />
              <div className="callout callout--soft">
                <p className="eyebrow">Executive summary</p>
                <strong>{result.executive_summary}</strong>
              </div>
              <div className="draft-block">
                <p className="eyebrow">Draft</p>
                <pre>{result.proposal_draft}</pre>
              </div>
              <div className="mini-list">
                <p className="eyebrow">Next steps</p>
                <ul>
                  {result.next_steps.map((item) => (
                    <li key={item}>{item}</li>
                  ))}
                </ul>
              </div>
            </div>
          ) : (
            <p className="panel-state">Generate a baseline proposal draft to inspect the output.</p>
          )}
        </aside>
      </div>
    </section>
  );
}
