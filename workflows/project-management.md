# Workflow: Project Management Control

## Trigger
Scheduled project review, milestone update, or delivery risk signal.

## Goal
Maintain an accurate project execution picture with distinct governance and execution-coordination responsibilities.

## Primary Agent Roles
- `PMO / Project Control Agent`: governance, RAID, steering summaries, slippage detection, and portfolio/control visibility
- `Project Management / Delivery Coordination Agent`: task activation, checkpoint sequencing, follow-up momentum, and deliverable-readiness tracking

## Steps
1. collect task, milestone, capacity, dependency, and meeting-note updates
2. `PMO / Project Control Agent` reconciles current delivery state against the control plan
3. detect slippage, blockers, and scope pressure
4. `Project Management / Delivery Coordination Agent` generates the active action list, follow-ups, and next checkpoint plan
5. flag items requiring leadership intervention
6. update project control record and execution follow-up state
7. route high-risk changes for CEO review

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
