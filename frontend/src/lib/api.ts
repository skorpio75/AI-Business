import type {
  AgentContract,
  ApprovalItem,
  DashboardSummary,
  KnowledgeQueryResponse,
  ProposalGenerationResponse,
  WorkflowRun,
} from "../types";

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

async function postJson<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error(`request_failed:${response.status}`);
  }

  return (await response.json()) as T;
}

export const apiClient = {
  getAgents(): Promise<AgentContract[]> {
    return getJson<AgentContract[]>("/agents");
  },

  getDashboardSummary(): Promise<DashboardSummary> {
    return getJson<DashboardSummary>("/dashboard/summary");
  },

  getWorkflowRuns(): Promise<WorkflowRun[]> {
    return getJson<WorkflowRun[]>("/workflows/runs");
  },

  getPendingApprovals(): Promise<ApprovalItem[]> {
    return getJson<ApprovalItem[]>("/approvals/pending");
  },

  runEmailWorkflow(payload: {
    subject: string;
    body: string;
    sender: string;
    thread_context?: string;
    risk_level: "low" | "medium" | "high";
  }): Promise<WorkflowRun> {
    return postJson<WorkflowRun>("/workflows/email-operations/run", payload);
  },

  runKnowledgeQna(payload: {
    question: string;
    limit: number;
  }): Promise<KnowledgeQueryResponse> {
    return postJson<KnowledgeQueryResponse>("/knowledge/qna", payload);
  },

  runProposalGeneration(payload: {
    client_name: string;
    opportunity_summary: string;
    desired_outcomes: string[];
    constraints: string[];
  }): Promise<ProposalGenerationResponse> {
    return postJson<ProposalGenerationResponse>("/workflows/proposal-generation/run", payload);
  },

  decideApproval(
    approvalId: string,
    payload: {
      decision: "approve" | "reject" | "edit";
      edited_reply?: string;
      note?: string;
    },
  ): Promise<ApprovalItem> {
    return postJson<ApprovalItem>(`/approvals/${approvalId}/decision`, payload);
  },
};
