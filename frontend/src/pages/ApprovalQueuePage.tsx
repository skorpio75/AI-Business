/* Copyright (c) Dario Pizzolante */
import { useDeferredValue, useEffect, useState } from "react";

import { StatusPill } from "../components/StatusPill";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Textarea } from "../components/ui/textarea";
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
  const [note, setNote] = useState("");
  const [editedReply, setEditedReply] = useState("");
  const [actionError, setActionError] = useState<string | null>(null);
  const [actionMessage, setActionMessage] = useState<string | null>(null);
  const [acting, setActing] = useState(false);
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
        setSelectedApprovalId((current) =>
          orderedApprovals.some((item) => item.id === current) ? current : orderedApprovals[0]?.id ?? null,
        );
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

  useEffect(() => {
    setEditedReply(selectedApproval?.draft_reply ?? "");
    setNote(selectedApproval?.decision_note ?? "");
    setActionError(null);
    setActionMessage(null);
  }, [selectedApprovalId, selectedApproval?.draft_reply, selectedApproval?.decision_note]);

  async function handleDecision(decision: "approve" | "reject" | "edit") {
    if (!selectedApproval) {
      return;
    }

    setActing(true);
    setActionError(null);
    setActionMessage(null);

    try {
      await apiClient.decideApproval(selectedApproval.id, {
        decision,
        edited_reply: editedReply || undefined,
        note: note || undefined,
      });
      const refreshed = await apiClient.getPendingApprovals();
      const orderedApprovals = [...refreshed].sort((left, right) =>
        right.created_at.localeCompare(left.created_at),
      );
      setApprovals(orderedApprovals);
      setSelectedApprovalId(
        decision === "edit"
          ? orderedApprovals.find((item) => item.id === selectedApproval.id)?.id ?? orderedApprovals[0]?.id ?? null
          : orderedApprovals[0]?.id ?? null,
      );
      setActionMessage(decision === "edit" ? "Draft updated and kept pending." : `Approval ${decision} completed.`);
    } catch (decisionError) {
      setActionError(decisionError instanceof Error ? decisionError.message : "unknown_error");
    } finally {
      setActing(false);
    }
  }

  return (
    <section className="page-grid">
      <div className="hero-card hero-card--amber">
        <div>
          <p className="eyebrow">Approval queue</p>
          <h2>Review pending items and resolve approval decisions from the UI.</h2>
        </div>
        <p className="hero-copy">
          This page reads `GET /approvals/pending` and posts approval decisions to
          `POST /approvals/:approval_id/decision`.
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
              <Input
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
                <Textarea value={editedReply} onChange={(event) => setEditedReply(event.target.value)} rows={10} />
              </div>
              <label className="form-field">
                <span>Decision note</span>
                <Textarea value={note} onChange={(event) => setNote(event.target.value)} rows={3} />
              </label>
              {actionError ? <p className="panel-state panel-state--error">{actionError}</p> : null}
              {actionMessage ? <p className="panel-state">{actionMessage}</p> : null}
              <div className="action-bar">
                <Button type="button" disabled={acting} onClick={() => void handleDecision("approve")}>
                  Approve
                </Button>
                <Button type="button" disabled={acting} onClick={() => void handleDecision("reject")} variant="outline">
                  Reject
                </Button>
                <Button
                  type="button"
                  disabled={acting || !editedReply.trim()}
                  onClick={() => void handleDecision("edit")}
                  variant="secondary"
                >
                  Save draft
                </Button>
              </div>
            </div>
          ) : (
            <p className="panel-state">Select a pending item to review its details.</p>
          )}
        </aside>
      </div>
    </section>
  );
}
