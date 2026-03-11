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

export type ViewKey = "workflow-monitor" | "approval-queue";
