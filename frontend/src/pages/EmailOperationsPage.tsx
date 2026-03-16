/* Copyright (c) Dario Pizzolante */
import { useState } from "react";

import { ModelRouteIndicator } from "../components/ModelRouteIndicator";
import { StatusPill } from "../components/StatusPill";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Select } from "../components/ui/select";
import { Textarea } from "../components/ui/textarea";
import { apiClient } from "../lib/api";
import { formatConfidence } from "../lib/format";
import type { WorkflowRun } from "../types";

type EmailOperationsPageProps = {
  onCreated(): void;
};

export function EmailOperationsPage({ onCreated }: EmailOperationsPageProps) {
  const [subject, setSubject] = useState("");
  const [sender, setSender] = useState("");
  const [body, setBody] = useState("");
  const [threadContext, setThreadContext] = useState("");
  const [riskLevel, setRiskLevel] = useState<"low" | "medium" | "high">("medium");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<WorkflowRun | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      const nextResult = await apiClient.runEmailWorkflow({
        subject,
        sender,
        body,
        thread_context: threadContext || undefined,
        risk_level: riskLevel,
      });
      setResult(nextResult);
      onCreated();
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "unknown_error");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="page-grid">
      <div className="hero-card">
        <div>
          <p className="eyebrow">Email operations</p>
          <h2>Run the existing email workflow from the UI.</h2>
        </div>
        <p className="hero-copy">
          This page submits to `POST /workflows/email-operations/run` and immediately feeds the
          approval queue.
        </p>
      </div>

      <div className="content-grid">
        <form className="panel form-panel" onSubmit={handleSubmit}>
          <div className="panel-header">
            <div>
              <p className="eyebrow">Workflow input</p>
              <h3>Compose a sample inbound email</h3>
            </div>
          </div>
          <label className="form-field">
            <span>Sender</span>
            <Input value={sender} onChange={(event) => setSender(event.target.value)} required />
          </label>
          <label className="form-field">
            <span>Subject</span>
            <Input value={subject} onChange={(event) => setSubject(event.target.value)} required />
          </label>
          <label className="form-field">
            <span>Body</span>
            <Textarea value={body} onChange={(event) => setBody(event.target.value)} rows={8} required />
          </label>
          <label className="form-field">
            <span>Thread context</span>
            <Textarea
              value={threadContext}
              onChange={(event) => setThreadContext(event.target.value)}
              rows={4}
            />
          </label>
          <label className="form-field">
            <span>Risk level</span>
            <Select value={riskLevel} onChange={(event) => setRiskLevel(event.target.value as typeof riskLevel)}>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </Select>
          </label>
          {error ? <p className="panel-state panel-state--error">{error}</p> : null}
          <Button className="refresh-button" type="submit" disabled={submitting}>
            {submitting ? "Running..." : "Run workflow"}
          </Button>
        </form>

        <aside className="panel panel--detail">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Latest result</p>
              <h3>{result?.intent ?? "No workflow run yet"}</h3>
            </div>
          </div>
          {result ? (
            <div className="detail-stack">
              <div className="detail-row">
                <span>Status</span>
                <StatusPill label={result.status.replace("_", " ")} tone="warning" />
              </div>
              <div className="detail-row">
                <span>Confidence</span>
                <strong>{formatConfidence(result.confidence)}</strong>
              </div>
              <div className="detail-row">
                <span>Approval ID</span>
                <code>{result.approval_id}</code>
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
              <div className="draft-block">
                <p className="eyebrow">Draft reply</p>
                <pre>{result.draft_reply}</pre>
              </div>
            </div>
          ) : (
            <p className="panel-state">Submit an email workflow to see the approval-ready result.</p>
          )}
        </aside>
      </div>
    </section>
  );
}
