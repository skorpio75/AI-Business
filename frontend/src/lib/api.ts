/* Copyright (c) Dario Pizzolante */
import type {
  AgentContract,
  ApprovalItem,
  ChiefAIPanel,
  CTOCIOPanel,
  DashboardSummary,
  FinancePanel,
  KnowledgeQueryResponse,
  PersonalAssistantContext,
  ProposalGenerationResponse,
  PublicLeadCaptureResponse,
  WorkflowTrace,
  WorkflowRun,
} from "../types";

function isLoopbackHostname(hostname: string): boolean {
  const normalized = hostname.trim().toLowerCase();
  return normalized === "localhost" || normalized === "127.0.0.1" || normalized === "::1" || normalized === "[::1]";
}

function remapLoopbackBaseUrlForLan(baseUrl: string): string {
  if (typeof window === "undefined" || !/^https?:\/\//.test(baseUrl)) {
    return baseUrl;
  }

  const browserHostname = window.location.hostname.trim();
  if (!browserHostname || isLoopbackHostname(browserHostname)) {
    return baseUrl;
  }

  try {
    const parsedBaseUrl = new URL(baseUrl);
    if (!isLoopbackHostname(parsedBaseUrl.hostname)) {
      return baseUrl;
    }

    parsedBaseUrl.hostname = browserHostname;
    return parsedBaseUrl.toString().replace(/\/$/, "");
  } catch {
    return baseUrl;
  }
}

function resolveApiBaseUrl(): string {
  const configuredBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim();
  if (!configuredBaseUrl) {
    if (typeof window !== "undefined") {
      return `${window.location.protocol}//${window.location.hostname}:8000`;
    }
    return "http://127.0.0.1:8000";
  }
  if (configuredBaseUrl === "same-origin") {
    return "";
  }
  return remapLoopbackBaseUrlForLan(configuredBaseUrl.replace(/\/$/, ""));
}

export const API_BASE_URL = resolveApiBaseUrl();

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

  getCtoCioPanel(): Promise<CTOCIOPanel> {
    return getJson<CTOCIOPanel>("/specialists/cto-cio/panel");
  },

  getFinancePanel(): Promise<FinancePanel> {
    return getJson<FinancePanel>("/specialists/finance/panel");
  },

  getChiefAiPanel(): Promise<ChiefAIPanel> {
    return getJson<ChiefAIPanel>("/specialists/chief-ai-digital-strategy/panel");
  },

  getPersonalAssistantContext(params?: {
    window_hours?: number;
    inbox_lookback_hours?: number;
    inbox_limit?: number;
    task_limit?: number;
    include_completed_tasks?: boolean;
  }): Promise<PersonalAssistantContext> {
    const search = new URLSearchParams();
    if (params?.window_hours) {
      search.set("window_hours", String(params.window_hours));
    }
    if (params?.inbox_lookback_hours) {
      search.set("inbox_lookback_hours", String(params.inbox_lookback_hours));
    }
    if (params?.inbox_limit) {
      search.set("inbox_limit", String(params.inbox_limit));
    }
    if (params?.task_limit) {
      search.set("task_limit", String(params.task_limit));
    }
    if (params?.include_completed_tasks) {
      search.set("include_completed_tasks", "true");
    }
    const suffix = search.size ? `?${search.toString()}` : "";
    return getJson<PersonalAssistantContext>(`/personal-assistant/context${suffix}`);
  },

  getWorkflowRuns(): Promise<WorkflowRun[]> {
    return getJson<WorkflowRun[]>("/workflows/runs");
  },

  getWorkflowTrace(workflowId: string): Promise<WorkflowTrace> {
    return getJson<WorkflowTrace>(`/audit/workflows/${workflowId}`);
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
    source_account_id?: string;
    source_message_id?: string;
    source_thread_id?: string;
    source_provider?: string;
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

  submitPublicBookingRequest(payload: {
    full_name: string;
    email: string;
    company?: string;
    role_title?: string;
    service_interest?: string;
    challenge_summary: string;
    preferred_timing?: string;
    website_path: string;
    consent_to_contact: boolean;
  }): Promise<PublicLeadCaptureResponse> {
    return postJson<PublicLeadCaptureResponse>("/public/booking-requests", payload);
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
