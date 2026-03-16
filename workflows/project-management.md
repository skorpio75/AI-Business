<!-- Copyright (c) Dario Pizzolante -->
# Workflow: Project Management Control

## Trigger
Scheduled project review, milestone update, or delivery risk signal.

## Pod Owner
`Delivery`

## Start Event
- `project.created`
- `milestone.updated`
- `risk.threshold_crossed`
- scheduled delivery review

## Goal
Maintain an accurate project execution picture with distinct governance and execution-coordination responsibilities.

## State Objects
- `project_state`
- `run_state`
- `approval_state` where material plan changes or client-facing commitments are involved

## Primary Agent Roles
- `PMO / Project Control Agent`: governance, RAID, steering summaries, slippage detection, and portfolio/control visibility
- `Project Management / Delivery Coordination Agent`: task activation, checkpoint sequencing, follow-up momentum, and deliverable-readiness tracking
- `BA / Requirements Agent`: updates requirements when scope or process understanding changes
- `Architect Agent`: contributes design-change impact and dependency implications
- `Risk / Watchdog Agent`: later surfaces missing approvals, slippage, and delivery anomalies across the chain

## Steps
1. collect task, milestone, capacity, dependency, and meeting-note updates
2. `PMO / Project Control Agent` reconciles current delivery state against the control plan
3. detect slippage, blockers, and scope pressure
4. `Project Management / Delivery Coordination Agent` generates the active action list, follow-ups, and next checkpoint plan
5. flag items requiring leadership intervention
6. update project control record and execution follow-up state
7. route high-risk changes for CEO review

## Emitted Events
- `project.control.updated`
- `requirements.updated`
- `risk.threshold_crossed`
- `approval.pending`
- `milestone.completed` when governance signals indicate a milestone close

## Approval Gates
- material plan changes, scope changes, or client-facing commitments require CEO approval in the MVP

## AI Steps
- blocker summarization
- action list prioritization
- stakeholder update drafting
- checkpoint and follow-up drafting

## Deterministic Steps
- schedule ingestion
- dependency checks
- milestone status update
- risk threshold evaluation
- approval routing for material plan changes
- audit logging

## Failure Handling
- incomplete task state -> mark review partial
- conflicting project records -> escalate for PM validation
- connector failure -> retry then hold planning update

## Audit Data
- project id
- review date
- milestone variance
- blocker count
- risk level
- recommended actions
- approval status
