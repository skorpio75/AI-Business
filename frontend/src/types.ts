export type WorkflowRun = {
  workflow_id: string;
  status: "pending_approval";
  approval_id: string;
  intent: string;
  confidence: number;
  draft_reply: string;
  provider_used: string;
  model_used: string;
  escalation_reason?: string | null;
};

export type ApprovalItem = {
  id: string;
  workflow_id: string;
  created_at: string;
  sender: string;
  subject: string;
  draft_reply: string;
  status: "pending" | "approved" | "rejected" | "edited";
  decision_note?: string | null;
};

export type AgentCapability = {
  id: string;
  name: string;
  description: string;
};

export type AgentKpi = {
  id: string;
  name: string;
  unit: string;
  description: string;
};

export type AgentDeploymentPolicy = {
  primary_track: "track_a_internal" | "track_b_client";
  replication_mode: "none" | "replicate_later";
  replication_notes?: string | null;
};

export type AgentRuntimeState = {
  status: "idle" | "running" | "waiting" | "blocked" | "disabled";
  last_run_at?: string | null;
  current_task?: string | null;
  last_error?: string | null;
  updated_at: string;
};

export type AgentContract = {
  agent_id: string;
  display_name: string;
  domain: "corporate" | "delivery" | "platform";
  role_summary: string;
  approval_class: "none" | "bounded" | "ceo_required";
  deployment: AgentDeploymentPolicy;
  capabilities: AgentCapability[];
  kpis: AgentKpi[];
  tools: string[];
  inputs: string[];
  outputs: string[];
  constraints: string[];
  runtime: AgentRuntimeState;
};

export type KnowledgeCitation = {
  title: string;
  source_path: string;
  snippet: string;
  score: number;
};

export type KnowledgeQueryResponse = {
  question: string;
  answer: string;
  citations: KnowledgeCitation[];
  grounded: boolean;
  provider_used: string;
  model_used: string;
};

export type ProposalGenerationResponse = {
  workflow_id: string;
  status: "completed";
  title: string;
  executive_summary: string;
  proposal_draft: string;
  next_steps: string[];
  provider_used: string;
  model_used: string;
};

export type DashboardKpi = {
  id: string;
  label: string;
  value: string;
  tone: "neutral" | "success" | "warning" | "critical";
  context: string;
  footnote?: string | null;
};

export type PersonalAssistantPriority = {
  title: string;
  reason: string;
  urgency: "low" | "medium" | "high";
};

export type ScheduleConflict = {
  title: string;
  detail: string;
  severity: "info" | "warning" | "critical";
};

export type PersonalAssistantQuickAction = {
  label: string;
  target_view: string;
  reason: string;
};

export type PersonalAssistantBrief = {
  priorities: PersonalAssistantPriority[];
  schedule_conflicts: ScheduleConflict[];
  quick_actions: PersonalAssistantQuickAction[];
  inbox_status: string;
  calendar_status: string;
};

export type DashboardSummary = {
  kpis: DashboardKpi[];
  personal_assistant: PersonalAssistantBrief;
};

export type ViewKey =
  | "workflow-monitor"
  | "approval-queue"
  | "agent-activity"
  | "agents-org"
  | "email-operations"
  | "knowledge-qna"
  | "proposal-generation";
