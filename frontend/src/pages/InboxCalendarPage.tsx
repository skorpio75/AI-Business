/* Copyright (c) Dario Pizzolante */
import { useEffect, useMemo, useState } from "react";

import { StatusPill } from "../components/StatusPill";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { apiClient } from "../lib/api";
import { formatDateTime, truncate } from "../lib/format";
import type { InboxMessage, PersonalAssistantContext, TodoTask, WorkflowRun } from "../types";

type InboxCalendarPageProps = {
  refreshToken: number;
  onDrafted(): void;
};

function inferTone(status?: string | null): "neutral" | "success" | "warning" | "critical" {
  if (status === "ok" || status === "sent") {
    return "success";
  }
  if (status === "degraded" || status === "pending") {
    return "warning";
  }
  if (status === "error") {
    return "critical";
  }
  return "neutral";
}

export function InboxCalendarPage({ refreshToken, onDrafted }: InboxCalendarPageProps) {
  const [context, setContext] = useState<PersonalAssistantContext | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lookbackHours, setLookbackHours] = useState(168);
  const [inboxLimit, setInboxLimit] = useState(20);
  const [taskLimit, setTaskLimit] = useState(20);
  const [selectedMessageId, setSelectedMessageId] = useState<string | null>(null);
  const [drafting, setDrafting] = useState(false);
  const [draftError, setDraftError] = useState<string | null>(null);
  const [draftResult, setDraftResult] = useState<WorkflowRun | null>(null);

  useEffect(() => {
    let active = true;

    async function loadContext() {
      setLoading(true);
      setError(null);
      try {
        const nextContext = await apiClient.getPersonalAssistantContext({
          window_hours: 24,
          inbox_lookback_hours: lookbackHours,
          inbox_limit: inboxLimit,
          task_limit: taskLimit,
        });
        if (!active) {
          return;
        }
        setContext(nextContext);
        setSelectedMessageId((current) =>
          nextContext.inbox_messages.some((item) => item.message_id === current)
            ? current
            : nextContext.inbox_messages[0]?.message_id ?? null,
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

    void loadContext();
    return () => {
      active = false;
    };
  }, [refreshToken, lookbackHours, inboxLimit, taskLimit]);

  const selectedMessage = useMemo<InboxMessage | null>(
    () => context?.inbox_messages.find((item) => item.message_id === selectedMessageId) ?? context?.inbox_messages[0] ?? null,
    [context, selectedMessageId],
  );

  const openTasks = useMemo<TodoTask[]>(
    () => (context?.todo_tasks ?? []).filter((task) => task.status !== "completed"),
    [context],
  );

  async function handleDraftFromInbox() {
    if (!selectedMessage) {
      return;
    }
    setDrafting(true);
    setDraftError(null);
    setDraftResult(null);
    try {
      const run = await apiClient.runEmailWorkflow({
        subject: selectedMessage.subject,
        body: selectedMessage.body_text,
        sender: selectedMessage.sender,
        risk_level: "medium",
        source_account_id: selectedMessage.account_id,
        source_message_id: selectedMessage.message_id,
        source_thread_id: selectedMessage.thread_id ?? undefined,
        source_provider: selectedMessage.metadata.provider,
      });
      setDraftResult(run);
      onDrafted();
    } catch (runError) {
      setDraftError(runError instanceof Error ? runError.message : "unknown_error");
    } finally {
      setDrafting(false);
    }
  }

  return (
    <section className="page-grid">
      <div className="hero-card hero-card--mint">
        <div>
          <p className="eyebrow">Inbox, calendar, and todos</p>
          <h2>Read live assistant context and launch approval-bound replies.</h2>
        </div>
        <p className="hero-copy">
          This page reads the configured provider context and lets you turn a real inbox message
          into an approval workflow that can later send through the active mail provider on approval.
        </p>
      </div>

      <section className="panel">
        <div className="panel-header panel-header--spread">
          <div>
            <p className="eyebrow">Live controls</p>
            <h3>Assistant read window</h3>
          </div>
          <div className="toolbar-row">
            <label className="form-field form-field--compact">
              <span>Inbox lookback (hours)</span>
              <Input
                type="number"
                min={1}
                max={720}
                value={lookbackHours}
                onChange={(event) => setLookbackHours(Number(event.target.value))}
              />
            </label>
            <label className="form-field form-field--compact">
              <span>Inbox limit</span>
              <Input
                type="number"
                min={1}
                max={100}
                value={inboxLimit}
                onChange={(event) => setInboxLimit(Number(event.target.value))}
              />
            </label>
            <label className="form-field form-field--compact">
              <span>Task limit</span>
              <Input
                type="number"
                min={1}
                max={100}
                value={taskLimit}
                onChange={(event) => setTaskLimit(Number(event.target.value))}
              />
            </label>
          </div>
        </div>
        <div className="tag-cloud">
          <StatusPill
            label={`inbox ${context?.inbox_health?.status ?? "unknown"}`}
            tone={inferTone(context?.inbox_health?.status)}
          />
          <StatusPill
            label={`calendar ${context?.calendar_health?.status ?? "unknown"}`}
            tone={inferTone(context?.calendar_health?.status)}
          />
          <StatusPill
            label={`tasks ${context?.tasks_health?.status ?? "unknown"}`}
            tone={inferTone(context?.tasks_health?.status)}
          />
          <StatusPill label={`${context?.inbox_messages.length ?? 0} inbox messages`} tone="neutral" />
          <StatusPill label={`${context?.calendar_events.length ?? 0} calendar events`} tone="neutral" />
          <StatusPill label={`${context?.todo_tasks.length ?? 0} tasks`} tone="neutral" />
        </div>
        {loading ? <p className="panel-state">Loading live assistant context...</p> : null}
        {error ? <p className="panel-state panel-state--error">{error}</p> : null}
      </section>

      <div className="content-grid">
        <section className="panel">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Inbox</p>
              <h3>Recent messages</h3>
            </div>
          </div>
          {!loading && !error && !(context?.inbox_messages.length) ? (
            <p className="panel-state">No inbox messages found in the current lookback window.</p>
          ) : null}
          <div className="stack-list">
            {context?.inbox_messages.map((message) => (
              <button
                key={message.message_id}
                type="button"
                className={`list-card ${selectedMessage?.message_id === message.message_id ? "list-card--active" : ""}`}
                onClick={() => setSelectedMessageId(message.message_id)}
              >
                <div className="list-card__topline">
                  <StatusPill label={message.is_unread ? "unread" : "read"} tone={message.is_unread ? "warning" : "neutral"} />
                  <span>{formatDateTime(message.received_at)}</span>
                </div>
                <h4>{message.subject}</h4>
                <p>{truncate(message.sender, 84)}</p>
                <div className="list-card__meta">
                  <span>{message.metadata.provider ?? "unknown-provider"}</span>
                  <span>{truncate(message.message_id, 24)}</span>
                </div>
              </button>
            ))}
          </div>
        </section>

        <aside className="panel panel--detail">
          <div className="panel-header">
            <div>
              <p className="eyebrow">Selected message</p>
              <h3>{selectedMessage?.subject ?? "No message selected"}</h3>
            </div>
          </div>
          {selectedMessage ? (
            <div className="detail-stack">
              <div className="detail-row">
                <span>From</span>
                <strong>{selectedMessage.sender}</strong>
              </div>
              <div className="detail-row">
                <span>Received</span>
                <strong>{formatDateTime(selectedMessage.received_at)}</strong>
              </div>
              <div className="detail-row">
                <span>Message ID</span>
                <code>{selectedMessage.message_id}</code>
              </div>
              <div className="detail-row">
                <span>Thread ID</span>
                <code>{selectedMessage.thread_id ?? "n/a"}</code>
              </div>
              <div className="draft-block">
                <p className="eyebrow">Message body</p>
                <pre>{selectedMessage.body_text || "(empty preview)"}</pre>
              </div>
              {draftError ? <p className="panel-state panel-state--error">{draftError}</p> : null}
              {draftResult ? (
                <div className="callout callout--soft">
                  <p className="eyebrow">Workflow queued</p>
                  <strong>{draftResult.approval_id}</strong>
                </div>
              ) : null}
              <Button className="refresh-button" type="button" disabled={drafting} onClick={() => void handleDraftFromInbox()}>
                {drafting ? "Drafting..." : "Draft reply workflow"}
              </Button>
            </div>
          ) : (
            <p className="panel-state">Select a live inbox message to inspect or draft a reply.</p>
          )}
        </aside>
      </div>

      <section className="panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">Calendar</p>
            <h3>Upcoming agenda</h3>
          </div>
        </div>
        {!loading && !error && !(context?.calendar_events.length) ? (
          <p className="panel-state">No calendar events found in the current assistant window.</p>
        ) : null}
        <div className="stack-list">
          {context?.calendar_events.map((event) => (
            <article key={event.event_id} className="list-card">
              <div className="list-card__topline">
                <StatusPill label={event.response_status.replace("_", " ")} tone={event.response_status === "declined" ? "critical" : event.response_status === "tentative" ? "warning" : "success"} />
                <span>{formatDateTime(event.start_at)}</span>
              </div>
              <h4>{event.title}</h4>
              <p>{event.organizer ?? "No organizer"}</p>
              <div className="list-card__meta">
                <span>{event.location || "No location"}</span>
                <span>{event.is_all_day ? "All day" : formatDateTime(event.end_at)}</span>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">Todos</p>
            <h3>Current task list</h3>
          </div>
        </div>
        {!loading && !error && !openTasks.length ? (
          <p className="panel-state">No open tasks found in the current assistant task list.</p>
        ) : null}
        <div className="stack-list">
          {openTasks.map((task) => (
            <article key={task.task_id} className="list-card">
              <div className="list-card__topline">
                <StatusPill label={task.priority} tone={task.priority === "high" ? "warning" : "neutral"} />
                <span>{task.due_at ? formatDateTime(task.due_at) : "No due date"}</span>
              </div>
              <h4>{task.title}</h4>
              <p>{truncate(task.body_text || "No task notes", 120)}</p>
              <div className="list-card__meta">
                <span>{task.status.replace("_", " ")}</span>
                <span>{task.metadata.provider ?? "unknown-provider"}</span>
              </div>
            </article>
          ))}
        </div>
      </section>
    </section>
  );
}
