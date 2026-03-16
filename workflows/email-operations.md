<!-- Copyright (c) Dario Pizzolante -->
# Workflow: Email Operations

## Trigger
A new inbound email is received.

## Pod Owner
`Growth` with `Email Agent` acting as a specialist overlay inside the workflow.

## Start Event
- `email.received`
- operator launch from Mission Control

## Goal
Produce a grounded draft reply and route it for approval.

## State Objects
- `run_state`
- `approval_state` when outbound send is requested

## Primary Agent Roles
- `Email Agent`: classify intent, retrieve context, draft the reply, and route approval
- `Knowledge Agent`: contributes evidence-backed retrieval context when grounding is needed
- `Mission Control Agent`: later supervises run visibility, approval status, and escalation state

## Steps
1. ingest inbound email
2. classify intent
3. retrieve relevant knowledge
4. generate draft reply
5. assign confidence score
6. route to approval queue
7. send only after approval

## Emitted Events
- `email.classified`
- `knowledge.retrieved`
- `approval.pending`
- `approval.approved` or `approval.rejected`
- `email.sent` when an approved send occurs

## Approval Gates
- any outbound send requires CEO approval

## AI Steps
- intent classification
- reply drafting
- confidence estimation

## Deterministic Steps
- email ingestion
- retrieval call
- approval routing
- outbound send
- audit logging

## Failure Handling
- missing knowledge -> manual review
- low confidence -> escalate
- connector failure -> retry then manual review

## Audit Data
- inbound message id
- workflow id
- prompt version
- model used
- confidence score
- approval status
