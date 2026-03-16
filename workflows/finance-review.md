<!-- Copyright (c) Dario Pizzolante -->
# Workflow: Finance Review

## Trigger
Scheduled daily/weekly finance snapshot or a manual CFO/CEO review request.

## Pod Owner
`Ops` with executive review output

## Start Event
- `finance.review.scheduled`
- manual CFO or CEO review request

## Goal
Produce a current financial view with risk flags, cashflow interpretation, and recommended actions.

## State Objects
- `run_state`
- later feeds company-level reporting and executive review state

## Primary Agent Roles
- `Finance Agent`: produce current cash and finance snapshot
- `Finance Ops Agent`: validate internal control and forecast-versus-actual signals
- `CFO Agent`: interpret financial posture and recommend strategic options
- `CEO Briefing Agent`: later consumes accepted finance summaries for executive synthesis

## Emitted Events
- `finance.snapshot.completed`
- `risk.threshold_crossed`
- `approval.pending` when high-risk findings require review
- `reporting.refresh_requested`

## Steps
1. collect revenue, expense, receivable, payable, and cash position data
2. validate completeness of the accounting snapshot
3. calculate cashflow, runway, margin, and collections indicators
4. detect anomalies and threshold breaches
5. generate finance commentary and recommended actions
6. route high-risk findings to CEO review
7. persist approved finance snapshot for reporting

## Approval Gates
- high-risk findings and executive actions require CEO review before they are treated as approved guidance

## AI Steps
- anomaly interpretation
- scenario commentary
- executive summary drafting

## Deterministic Steps
- accounting data retrieval
- KPI calculation
- threshold checks
- snapshot persistence
- approval routing for high-risk cases
- audit logging

## Failure Handling
- incomplete accounting data -> mark snapshot partial and escalate
- conflicting balances -> block publication
- connector timeout -> retry then fallback to latest confirmed snapshot

## Audit Data
- snapshot timestamp
- data source timestamps
- cash balance
- runway estimate
- anomaly ids
- recommendation summary
- approval status
