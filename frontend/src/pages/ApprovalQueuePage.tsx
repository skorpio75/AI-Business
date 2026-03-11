import { useDeferredValue, useEffect, useState } from "react";

import { StatusPill } from "../components/StatusPill";
import { apiClient } from "../lib/api";
import { formatDateTime, truncate } from "../lib/format";
import type { ApprovalItem } from "../types";

type ApprovalQueuePageProps = {
  refreshToken: number;
};

export function ApprovalQueuePage({ refreshToken }: ApprovalQueuePageProps) {
  const [approvals, setApprovals] = useState<ApprovalItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedApprovalId, setSelectedApprovalId] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const deferredQuery = useDeferredValue(query);

  useEffect(() => {
    let active = true;

    async function loadApprovals() {
      setLoading(true);
      setError(null);

      try {
        const nextApprovals = await apiClient.getPendingApprovals();
        if (!active) {
          return;
        }

        const orderedApprovals = [...nextApprovals].sort((left, right) =>
          right.created_at.localeCompare(left.created_at),
        );
        setApprovals(orderedApprovals);
        setSelectedApprovalId((current) => current ?? orderedApprovals[0]?.id ?? null);
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

    void loadApprovals();
    return () => {
      active = false;
    };
  }, [refreshToken]);

  const normalizedQuery = deferredQuery.trim().toLowerCase();
  const filteredApprovals = normalizedQuery
    ? approvals.filter((item) => {
        const haystack = `${item.sender} ${item.subject} ${item.workflow_id}`.toLowerCase();
        return haystack.includes(normalizedQuery);
      })
    : approvals;

  const selectedApproval =
    filteredApprovals.find((item) => item.id === selectedApprovalId) ??
    filteredApprovals[0] ??
    null;

  return (
    <section className="page-grid">
      <div className="hero-card hero-card--amber">
        <div>
          <p className="eyebrow">Approval queue</p>
          <h2>Review pending items without committing decisions yet.</h2>
        </div>
        <p className="hero-copy">
          This page reads `GET /approvals/pending`. Decision actions stay out of scope until
          `P3-T08`.
        </p>
      </div>

      <div className="content-grid">
        <section className="panel">
          <div className="panel-header panel-header--spread">
            <div>
              <p className="eyebrow">Pending approvals</p>
              <h3>CEO review inbox</h3>
            </div>
            <label className="search-field">
              <span>Filter</span>
              <input
                value={query}
                onChange={(event) => setQuery(event.target.value)}
                placeholder="Sender, subject, workflow id"
              />
            </label>
          </div>
          {loading ? <p className="panel-state">Loading approvals...</p> : null}
          {error ? <p className="panel-state panel-state--error">{error}</p> : null}
          {!loading && !error && filteredApprovals.length === 0 ? (
            <p className="panel-state">No pending approvals match the current filter.</p>
          ) : null}
          <div className="stack-list">
            {filteredApprovals.map((item) => (
              <button
                key={item.id}
                className={`list-card ${selectedApproval?.id === item.id ? "list-card--active" : ""}`}
                type="button"
                onClick={() => setSelectedApprovalId(item.id)}
              >
                <div className="list-card__topline">
                  <StatusPill label={item.status} tone="warning" />
                  <span>{formatDateTime(item.created_at)}</span>
                </div>
                <h4>{item.subject}</h4>
                <p>{truncate(item.sender, 72)}</p>
                <div className="list-card__meta">
                  <span>{truncate(item.workflow_id, 18)}</span>
                  <span>{truncate(item.id, 18)}</span>
                </div>
              </button>
            ))}
          </div>
        </section>

        <aside className="panel panel--detail">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Approval detail</p>
              <h3>{selectedApproval?.subject ?? "No approval selected"}</h3>
            </div>
          </div>
          {selectedApproval ? (
            <div className="detail-stack">
              <div className="detail-row">
                <span>Sender</span>
                <strong>{selectedApproval.sender}</strong>
              </div>
              <div className="detail-row">
                <span>Created</span>
                <strong>{formatDateTime(selectedApproval.created_at)}</strong>
              </div>
              <div className="detail-row">
                <span>Workflow</span>
                <code>{selectedApproval.workflow_id}</code>
              </div>
              <div className="detail-row">
                <span>Approval</span>
                <code>{selectedApproval.id}</code>
              </div>
              <div className="draft-block">
                <p className="eyebrow">Draft reply</p>
                <pre>{selectedApproval.draft_reply}</pre>
              </div>
              <div className="action-bar action-bar--disabled">
                <button type="button" disabled>
                  Approve
                </button>
                <button type="button" disabled>
                  Reject
                </button>
                <button type="button" disabled>
                  Edit
                </button>
              </div>
              <p className="muted-note">
                Decision mutations are intentionally deferred to `P3-T08` so the page ships
                before approval-write behavior is added.
              </p>
            </div>
          ) : (
            <p className="panel-state">Select a pending item to review its details.</p>
          )}
        </aside>
      </div>
    </section>
  );
}
