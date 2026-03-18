/* Copyright (c) Dario Pizzolante */
export type WorkflowRun = {
  workflow_id: string;
  status: "pending_approval" | "completed";
  approval_id: string;
  intent: string;
  confidence: number;
  draft_reply: string;
  provider_used: string;
  model_used: string;
  local_llm_invoked: boolean;
  cloud_llm_invoked: boolean;
  llm_diagnostic_code?: string | null;
  llm_diagnostic_detail?: string | null;
  escalation_reason?: string | null;
  approval_status: "pending" | "approved" | "rejected" | "edited";
  send_status: "pending" | "sent" | "not_applicable";
  sent_at?: string | null;
  source_provider?: string | null;
  source_message_id?: string | null;
};

export type AgentRunRecord = {
  agent_run_id: string;
  tenant_id: string;
  track: "track_a_internal" | "track_b_client";
  agent_id: string;
  agent_family: string;
  mode: "internal_operating" | "client_delivery" | "client_facing_service";
  status: "started" | "completed" | "failed" | "waiting" | "blocked";
  started_at: string;
  ended_at?: string | null;
  workflow_id?: string | null;
  run_id?: string | null;
  step_id?: string | null;
  parent_agent_run_id?: string | null;
  trigger_event_name?: string | null;
  input_ref?: string | null;
  output_ref?: string | null;
  autonomy_class?: "assistant" | "supervised_executor" | "bounded_autonomous" | "approval_gated" | null;
  approval_class?: "none" | "bounded" | "ceo_required" | null;
  provider_used?: string | null;
  model_used?: string | null;
  routing_path?: string | null;
  fallback_mode?: string | null;
  confidence?: number | null;
  trace_ref?: string | null;
  error_code?: string | null;
  error_detail?: string | null;
};

export type AuditEventRecord = {
  audit_event_id: string;
  tenant_id: string;
  track: "track_a_internal" | "track_b_client";
  occurred_at: string;
  event_name: string;
  entity_type: string;
  entity_id: string;
  actor_type: string;
  actor_id: string;
  status: string;
  workflow_id?: string | null;
  run_id?: string | null;
  step_id?: string | null;
  agent_run_id?: string | null;
  approval_id?: string | null;
  approval_class?: "none" | "bounded" | "ceo_required" | null;
  autonomy_class?: "assistant" | "supervised_executor" | "bounded_autonomous" | "approval_gated" | null;
  tool_id?: string | null;
  provider_used?: string | null;
  model_used?: string | null;
  routing_path?: string | null;
  fallback_mode?: string | null;
  trace_ref?: string | null;
  payload_ref_or_inline?: Record<string, unknown> | string | null;
  state_diff_ref?: string | null;
  error_code?: string | null;
  error_detail?: string | null;
};

export type WorkflowTrace = {
  workflow_id: string;
  workflow_run?: WorkflowRun | null;
  approval?: ApprovalItem | null;
  agent_runs: AgentRunRecord[];
  audit_events: AuditEventRecord[];
};

export type ToolProfileSummary = {
  operating_mode: "internal_operating" | "client_delivery" | "client_facing_service";
  operating_mode_label: string;
  profile_id: string;
  profile_summary: string;
};

export type GovernedMetadataSummary = {
  pod_label?: string | null;
  family_id?: string | null;
  family_label?: string | null;
  primary_track_label: string;
  operating_mode_labels: string[];
  approval_label: string;
  autonomy_label: string;
  replication_label: string;
  routing_posture: "DO-C" | "DO-G" | "GW-R" | "DT-H" | "UNSPECIFIED";
  routing_posture_label: string;
  routing_posture_summary: string;
  operating_model_label: string;
  operating_model_summary: string;
  tool_profiles: ToolProfileSummary[];
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
  source_account_id?: string | null;
  source_message_id?: string | null;
  source_thread_id?: string | null;
  source_provider?: string | null;
  send_status: "pending" | "sent" | "not_applicable";
  send_detail?: string | null;
  sent_at?: string | null;
};

export type InboxMessage = {
  message_id: string;
  thread_id?: string | null;
  account_id: string;
  folder: "inbox" | "sent" | "archive";
  direction: "inbound" | "outbound";
  sender: string;
  recipients: string[];
  subject: string;
  body_text: string;
  received_at: string;
  is_unread: boolean;
  labels: string[];
  metadata: Record<string, string>;
};

export type CalendarEvent = {
  event_id: string;
  calendar_id: string;
  title: string;
  start_at: string;
  end_at: string;
  organizer?: string | null;
  attendees: string[];
  location?: string | null;
  description?: string | null;
  response_status: "accepted" | "tentative" | "declined" | "needs_action";
  is_all_day: boolean;
  metadata: Record<string, string>;
};

export type TodoTask = {
  task_id: string;
  list_id: string;
  title: string;
  body_text?: string | null;
  due_at?: string | null;
  completed_at?: string | null;
  status: "not_started" | "in_progress" | "completed" | "deferred" | "waiting";
  priority: "low" | "normal" | "high";
  web_link?: string | null;
  metadata: Record<string, string>;
};

export type ConnectorHealth = {
  connector_id: string;
  status: "ok" | "degraded" | "error";
  checked_at: string;
  detail?: string | null;
};

export type PersonalAssistantContext = {
  account_id: string;
  calendar_id: string;
  task_list_id: string;
  window_start: string;
  window_end: string;
  inbox_messages: InboxMessage[];
  calendar_events: CalendarEvent[];
  todo_tasks: TodoTask[];
  inbox_health?: ConnectorHealth | null;
  calendar_health?: ConnectorHealth | null;
  tasks_health?: ConnectorHealth | null;
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
  pod?: "growth" | "delivery" | "ops" | "executive" | "specialist_overlay";
  family_id?: string | null;
  operating_modes?: ("internal_operating" | "client_delivery" | "client_facing_service")[];
  role_summary: string;
  approval_class: "none" | "bounded" | "ceo_required";
  autonomy_class: "assistant" | "supervised_executor" | "bounded_autonomous" | "approval_gated";
  tool_profile_by_mode?: Record<string, string>;
  deployment: AgentDeploymentPolicy;
  capabilities: AgentCapability[];
  kpis: AgentKpi[];
  tools: string[];
  inputs: string[];
  outputs: string[];
  constraints: string[];
  runtime: AgentRuntimeState;
  governed_metadata?: GovernedMetadataSummary | null;
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
  local_llm_invoked: boolean;
  cloud_llm_invoked: boolean;
  llm_diagnostic_code?: string | null;
  llm_diagnostic_detail?: string | null;
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
  local_llm_invoked: boolean;
  cloud_llm_invoked: boolean;
  llm_diagnostic_code?: string | null;
  llm_diagnostic_detail?: string | null;
};

export type PublicLeadCaptureResponse = {
  submission_id: string;
  lead_id: string;
  status: "received";
  source_class: "website_form";
  submission_kind: "booking_request";
  materialization_status: "materialized";
  received_at: string;
  message: string;
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

export type CTOCIOScopeInsight = {
  insight_id: string;
  title: string;
  summary: string;
  focus_area: "customer_scope" | "architecture" | "internal_platform";
  tone: "neutral" | "success" | "warning" | "critical";
};

export type StrategyOption = {
  option_id: string;
  title: string;
  summary: string;
  benefits: string[];
  tradeoffs: string[];
  recommended_when: string;
};

export type ArchitectureAdvice = {
  current_state: string;
  target_state: string;
  key_constraints: string[];
  proposed_changes: string[];
  risks: string[];
};

export type ImprovementBacklogItem = {
  item_id: string;
  title: string;
  rationale: string;
  priority: "now" | "next" | "later";
  impact: "low" | "medium" | "high";
  effort: "small" | "medium" | "large";
  owner_hint?: string | null;
};

export type CTOCIOPanel = {
  agent_id: string;
  display_name: string;
  role_summary: string;
  primary_track: "track_a_internal" | "track_b_client";
  operating_modes: string[];
  tool_profile_by_mode: Record<string, string>;
  governed_metadata: GovernedMetadataSummary;
  provider_used: string;
  model_used: string;
  local_llm_invoked: boolean;
  cloud_llm_invoked: boolean;
  llm_diagnostic_code?: string | null;
  llm_diagnostic_detail?: string | null;
  scope_insights: CTOCIOScopeInsight[];
  strategy_options: StrategyOption[];
  architecture_advice: ArchitectureAdvice;
  internal_improvement_backlog: ImprovementBacklogItem[];
  approval_required: boolean;
};

export type ReconciliationRule = {
  rule_id: string;
  description: string;
  severity: "warning" | "blocking";
};

export type ReconciliationException = {
  exception_id: string;
  summary: string;
  impacted_records: string[];
  severity: "warning" | "material" | "critical";
  recommended_action: string;
};

export type CloseChecklistItem = {
  item_id: string;
  title: string;
  owner: string;
  status: "pending" | "in_progress" | "completed" | "blocked";
  notes?: string | null;
};

export type FinancialScenario = {
  scenario_id: string;
  title: string;
  horizon: "30_days" | "90_days" | "12_months";
  assumptions: string[];
  projected_outcomes: string[];
  risks: string[];
};

export type FinancePanelAgentSummary = {
  agent_id: string;
  display_name: string;
  role_summary: string;
  primary_track: "track_a_internal" | "track_b_client";
  operating_modes: string[];
  tool_profile_by_mode: Record<string, string>;
  approval_class: "none" | "bounded" | "ceo_required";
  autonomy_class: "assistant" | "supervised_executor" | "bounded_autonomous" | "approval_gated";
  governed_metadata: GovernedMetadataSummary;
};

export type FinancePanel = {
  agents: FinancePanelAgentSummary[];
  reconciliation_rules: ReconciliationRule[];
  accounting_exceptions: ReconciliationException[];
  close_checklist: CloseChecklistItem[];
  accounting_ready_exports: string[];
  scenarios: FinancialScenario[];
  cashflow_risks: string[];
  recommendations: string[];
  executive_summary: string;
  approval_required: boolean;
};

export type OpportunityMapItem = {
  opportunity_id: string;
  title: string;
  problem_statement: string;
  expected_value: string;
  priority: "now" | "next" | "later";
  dependencies: string[];
};

export type DeliveryBlueprintPhase = {
  phase_id: string;
  title: string;
  objectives: string[];
  deliverables: string[];
  risks: string[];
};

export type MaturityDimension = {
  dimension: string;
  current_level: "ad_hoc" | "emerging" | "repeatable" | "managed" | "optimized";
  target_level: "ad_hoc" | "emerging" | "repeatable" | "managed" | "optimized";
  gap_summary: string;
  next_actions: string[];
};

export type ChiefAIScopeSignal = {
  signal_id: string;
  title: string;
  summary: string;
  focus_area: "offer_design" | "delivery_controls" | "commercialization";
  tone: "neutral" | "success" | "warning" | "critical";
};

export type ChiefAIPanel = {
  agent_id: string;
  display_name: string;
  role_summary: string;
  primary_track: "track_a_internal" | "track_b_client";
  operating_modes: string[];
  tool_profile_by_mode: Record<string, string>;
  governed_metadata: GovernedMetadataSummary;
  provider_used: string;
  model_used: string;
  local_llm_invoked: boolean;
  cloud_llm_invoked: boolean;
  llm_diagnostic_code?: string | null;
  llm_diagnostic_detail?: string | null;
  executive_summary: string;
  scope_signals: ChiefAIScopeSignal[];
  opportunity_map: OpportunityMapItem[];
  delivery_blueprint: DeliveryBlueprintPhase[];
  maturity_model: MaturityDimension[];
  approval_required: boolean;
};

export type ViewKey =
  | "workflow-monitor"
  | "approval-queue"
  | "agent-activity"
  | "agents-org"
  | "cto-cio"
  | "finance-cockpit"
  | "chief-ai-strategy"
  | "inbox-calendar"
  | "email-operations"
  | "knowledge-qna"
  | "proposal-generation";
