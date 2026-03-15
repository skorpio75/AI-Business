import { useState } from "react";

import { ModelRouteIndicator } from "../components/ModelRouteIndicator";
import { StatusPill } from "../components/StatusPill";
import { Button } from "../components/ui/button";
import { Select } from "../components/ui/select";
import { Textarea } from "../components/ui/textarea";
import { apiClient } from "../lib/api";
import type { KnowledgeQueryResponse } from "../types";

export function KnowledgeQnaPage() {
  const [question, setQuestion] = useState("");
  const [limit, setLimit] = useState(3);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<KnowledgeQueryResponse | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      const nextResult = await apiClient.runKnowledgeQna({ question, limit });
      setResult(nextResult);
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "unknown_error");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="page-grid">
      <div className="hero-card hero-card--mint">
        <div>
          <p className="eyebrow">Knowledge Q&A</p>
          <h2>Ask grounded questions against the internal knowledge store.</h2>
        </div>
        <p className="hero-copy">
          This page submits to `POST /knowledge/qna` and returns the answer plus source citations.
        </p>
      </div>

      <div className="content-grid">
        <form className="panel form-panel" onSubmit={handleSubmit}>
          <div className="panel-header">
            <div>
              <p className="eyebrow">Question</p>
              <h3>Knowledge query</h3>
            </div>
          </div>
          <label className="form-field">
            <span>Question</span>
            <Textarea value={question} onChange={(event) => setQuestion(event.target.value)} rows={6} required />
          </label>
          <label className="form-field">
            <span>Source limit</span>
            <Select value={limit} onChange={(event) => setLimit(Number(event.target.value))}>
              <option value={2}>2</option>
              <option value={3}>3</option>
              <option value={5}>5</option>
            </Select>
          </label>
          {error ? <p className="panel-state panel-state--error">{error}</p> : null}
          <Button className="refresh-button" type="submit" disabled={submitting}>
            {submitting ? "Searching..." : "Ask question"}
          </Button>
        </form>

        <aside className="panel panel--detail">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Answer</p>
              <h3>{result?.grounded ? "Grounded response" : "No answer yet"}</h3>
            </div>
          </div>
          {result ? (
            <div className="detail-stack">
              <div className="detail-row">
                <span>Grounded</span>
                <StatusPill label={result.grounded ? "yes" : "no"} tone={result.grounded ? "success" : "critical"} />
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
              <div className="draft-block">
                <p className="eyebrow">Answer</p>
                <pre>{result.answer}</pre>
              </div>
              <div className="mini-list">
                <p className="eyebrow">Citations</p>
                <ul>
                  {result.citations.map((citation) => (
                    <li key={`${citation.source_path}-${citation.title}`}>
                      <strong>{citation.title}</strong>: {citation.snippet}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ) : (
            <p className="panel-state">Ask a grounded question to see the answer and source evidence.</p>
          )}
        </aside>
      </div>
    </section>
  );
}
