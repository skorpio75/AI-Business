import type { ApprovalItem, WorkflowRun } from "../types";

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      Accept: "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`request_failed:${response.status}`);
  }

  return (await response.json()) as T;
}

export const apiClient = {
  getWorkflowRuns(): Promise<WorkflowRun[]> {
    return getJson<WorkflowRun[]>("/workflows/runs");
  },

  getPendingApprovals(): Promise<ApprovalItem[]> {
    return getJson<ApprovalItem[]>("/approvals/pending");
  },
};
