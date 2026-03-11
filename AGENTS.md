# Agents

## Purpose
This document lists the canonical agents used to run an IT freelancer company with one human CEO.

## Governance
- CEO is the sole human approver for high-risk decisions.
- Agents can execute routine tasks within workflow and policy constraints.
- No autonomous external commitment in MVP without CEO approval.
- Track 1 internal agents own their own state and memory. If an agent pattern is reused for Track 2 client services, it must be replicated as a separate agent/instance, not shared.

## Corporate Function Agents
### Email Agent
- classify inbound email
- retrieve context
- draft replies
- escalate low-confidence cases

### Personal Assistant Agent
- read inbox and calendar events
- detect commitments, deadlines, and conflicts
- generate prioritized daily action list
- draft quick replies and meeting prep notes

### Billing Agent
- generate invoices from approved timesheets/deliverables
- track payment status and reminders
- escalate overdue receivables

### Accountant Agent
- maintain bookkeeping records and journal consistency
- reconcile invoices, payments, and expense entries
- prepare accounting-ready exports and period-close checklists

### CFO Agent
- provide financial strategy recommendations and scenario planning
- monitor profitability, pricing, and cashflow risk
- advise CEO on investment, cost control, and growth decisions

### Finance Agent
- produce cashflow snapshots
- track revenue, expenses, and runway
- flag financial risks and anomalies

### Procurement (PO) Agent
- draft and track purchase orders
- validate budget limits before submission
- route approval for external commitments

### Reporting Agent
- generate weekly/monthly business reports
- consolidate operations and delivery KPIs

### Compliance/Contract Agent
- track contract obligations and milestones
- flag legal/compliance deadlines
- draft non-binding summaries for CEO review

### CTO/CIO Agent
- advise on client technology strategy based on scope and context
- provide architecture and delivery counsel for proposals and execution
- continuously assess and improve internal platform architecture, reliability, and tooling
- identify technical debt, optimization opportunities, and modernization priorities
- internal-first contract; replicate later for Track 2 CIO/CTO service offers without sharing Track 1 state

### Chief AI / Digital Strategy Agent
- advise clients on AI, digitalization, AI engineering, and data engineering opportunities
- translate customer scope into practical AI/data roadmaps and delivery plans
- provide implementation guidance for AI products, automations, and data platforms
- track AI capability maturity and prioritize continuous improvement actions
- internal-first contract; replicate later for Track 2 AI/digital strategy service offers without sharing Track 1 state

### Document Agent
- classify documents
- extract structured data
- route for processing

## Service Delivery Agents
### Knowledge Agent
- answer grounded questions from internal documents
- provide evidence-backed outputs

### Project Management Agent
- maintain project plan, tasks, and deadlines
- produce delivery forecasts and risk flags

### Delivery Agent
- orchestrate delivery checklists per engagement
- track milestone readiness and handoff state

### Quality Management Agent
- run quality gates before deliverable release
- enforce definition-of-done checks

### Consulting Support Agent
- prepare research-backed draft recommendations
- retrieve relevant internal/external context

### Documentation Agent
- generate and maintain project documentation packs
- ensure versioned artifacts for handover

### Testing/QA Agent
- generate and execute test plans
- summarize defects and release-readiness signals

### Ops Agent
- assist with internal operations and runbooks
- support release checklists and execution hygiene

## Approval Principle
No sensitive external action is sent automatically in MVP. CEO approval is required before execution for:
- money movement, invoicing release, and purchasing commitments
- contract/legal communications
- client-facing final deliverables
