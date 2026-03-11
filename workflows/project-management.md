# Workflow: Project Management Control

## Trigger
Scheduled project review, milestone update, or delivery risk signal.

## Goal
Maintain an accurate project execution picture with priorities, deadline risks, and recommended interventions.

## Steps
1. collect task, milestone, capacity, and dependency updates
2. reconcile current delivery state against the plan
3. detect slippage, blockers, and scope pressure
4. generate a prioritized action list and stakeholder notes
5. flag items requiring leadership intervention
6. update project control record
7. route high-risk changes for CEO review

## AI Steps
- blocker summarization
- action list prioritization
- stakeholder update drafting

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
